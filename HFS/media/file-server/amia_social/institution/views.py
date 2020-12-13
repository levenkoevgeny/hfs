from django.shortcuts import render
from django.views import View
from django.shortcuts import get_object_or_404

from .models import Institution, Vacancy, LanguageWithLevelVacancy, RespondedVacancy
from django.contrib.auth.mixins import LoginRequiredMixin
from .filters import VacancyFilterForProfile
from django.core.paginator import Paginator
from .forms import VacancyForm, LanguageWithLevelVacancyForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db import transaction
from django.http import JsonResponse
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


class SubscriptionAnswer:
    def __init__(self, last_name, vacancy_name, vacancy_id, count, img_url=None):
        self.last_name = last_name
        self.vacancy_name = vacancy_name
        self.vacancy_id = vacancy_id
        self.count = count
        self.img_url = img_url


class SearchView(LoginRequiredMixin, View):
    def get(self, request):
        institutions = Institution.objects.all()
        vacancies = Vacancy.objects.all().order_by('-date_added')[:5]

        f = VacancyFilterForProfile(request.GET, queryset=Vacancy.objects.all().order_by('-pk'))
        paginator = Paginator(f.qs, 50)
        page = request.GET.get('page')
        vacancies_search = paginator.get_page(page)

        return render(request, 'institution/vacancies/vacancy_search.html', {
            'institutions': institutions,
            'vacancies': vacancies,
            'vacancies_search': vacancies_search,
            'filter': f,
        })


class InstitutionVacancyView(LoginRequiredMixin, View):
    def get(self, request, institution_id):
        institution = get_object_or_404(Institution, pk=institution_id)
        return render(request, 'institution/vacancies/vacancy_institution.html', {
            'institution': institution,
        })

    def post(self, request):
        pass


class VacancyAddView(LoginRequiredMixin, View):

    def get(self, request):
        form_main = VacancyForm
        form_language = LanguageWithLevelVacancyForm
        return render(request, 'institution/vacancies/vacancy_input_form.html', {
            'form': form_main,
            'form_language': form_language,
        })

    @transaction.atomic
    def post(self, request):
        form = VacancyForm(request.POST)
        form_language = LanguageWithLevelVacancyForm(request.POST)
        if form.is_valid() and form_language.is_valid():
            vacancy_new = form.save()
            language_with_level = form_language.save(commit=False)
            language_with_level.vacancy = vacancy_new
            language_with_level.save()
            return HttpResponseRedirect(reverse('hr:main'))
        else:
            return render(request, 'institution/vacancies/vacancy_input_form.html', {
                'form': form, 'form_language': form_language
            })


class VacancyUpdateView(LoginRequiredMixin, View):
    def get(self, request, vacancy_id):
        obj = get_object_or_404(Vacancy, pk=vacancy_id)
        lang_obj = LanguageWithLevelVacancy.objects.filter(vacancy_id=obj.id).first()
        form = VacancyForm(instance=obj)
        form_language = LanguageWithLevelVacancyForm(instance=lang_obj)
        return render(request, 'institution/vacancies/vacancy_update_form.html', {
            'form': form,
            'form_language': form_language,
            'obj': obj,
        })

    @transaction.atomic
    def post(self, request, vacancy_id):
        obj = get_object_or_404(Vacancy, pk=vacancy_id)
        lang_obj = LanguageWithLevelVacancy.objects.filter(vacancy_id=obj.id).first()
        form = VacancyForm(request.POST, instance=obj)
        form_language = LanguageWithLevelVacancyForm(request.POST, instance=lang_obj)
        if form.is_valid() and form_language.is_valid():
            vacancy_new = form.save()
            language_with_level = form_language.save(commit=False)
            language_with_level.vacancy = vacancy_new
            language_with_level.save()
            return HttpResponseRedirect(reverse('hr:main'))
        else:
            return render(request, 'institution/vacancies/vacancy_input_form.html', {
                'form': form, 'form_language': form_language
            })


def subscription(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        sign = int(request.POST['subscribe_sign'])
        institution = get_object_or_404(Institution, pk=request.POST['institution_id'])
        if sign == -1:
            institution.subscribers.add(request.user.socialprofile)
            last_name = str(request.user.socialprofile.last_name)

            return JsonResponse({'last_name': last_name, 'sign': '1'})
        if sign == 1:
            institution.subscribers.remove(request.user.socialprofile)
            last_name = str(request.user.socialprofile.last_name)
            return JsonResponse({'last_name': last_name, 'sign': '-1'})


def vacancy_response(request):
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        sign = int(request.POST['response_sign'])
        vacancy = get_object_or_404(Vacancy, pk=request.POST['vacancy_id'])
        if sign == -1:
            vacancy.responded.add(request.user.socialprofile)
            last_name = str(request.user.socialprofile.last_name)
            if request.user.socialprofile.profile_img:
                img_url = request.user.socialprofile.profile_img.url
                sub_answer = SubscriptionAnswer(last_name, vacancy.vacancy, vacancy.id, vacancy.responded.count(), img_url)
            else:
                sub_answer = SubscriptionAnswer(last_name, vacancy.vacancy, vacancy.id, vacancy.responded.count())
            sub_answer_json = json.dumps(sub_answer .__dict__)
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                'hr',
                {
                    "type": "hr.message",
                    "message": sub_answer_json,
                }
            )

            return JsonResponse({'last_name': last_name, 'sign': '1', 'vacancy_id': vacancy.id})
        if sign == 1:
            vacancy.responded.remove(request.user.socialprofile)
            last_name = str(request.user.socialprofile.last_name)

            if request.user.socialprofile.profile_img:
                img_url = request.user.socialprofile.profile_img.url
                sub_answer = SubscriptionAnswer(last_name, vacancy.vacancy, vacancy.id, vacancy.responded.count(),
                                                img_url)
            else:
                sub_answer = SubscriptionAnswer(last_name, vacancy.vacancy, vacancy.id, vacancy.responded.count())
            sub_answer_json = json.dumps(sub_answer.__dict__)
            channel_layer = get_channel_layer()

            async_to_sync(channel_layer.group_send)(
                'hr',
                {
                    "type": "hr.message",
                    "message": sub_answer_json,
                }
            )
            return JsonResponse({'last_name': last_name, 'sign': '-1', 'vacancy_id': vacancy.id})


class VacancyDelete(DeleteView):
    template_name = 'institution/vacancies/vacancy_confirm_delete.html'
    model = Vacancy
    success_url = reverse_lazy('hr:main')




