from django.shortcuts import render
from django.views import View
from .models import SocialProfile, EducationWithInfo, WorkExperience, LanguageWithLevel
from django.shortcuts import get_object_or_404
from .forms import RegistrationForm, ProfileImageForm, PersonalDataForm, EducationWithInfoForm, WorkExperienceForm, InterestForm, SkillForm, LanguageWithLevelForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.db import transaction
from django.contrib.auth.mixins import LoginRequiredMixin


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, profile_id):
        profile_data = get_object_or_404(SocialProfile, pk=profile_id)
        return render(request, 'social_profile/profile.html', {
            'profile': profile_data
        })

    def post(self, request, profile_id):
        pass


class ProfileImageUpdateView(LoginRequiredMixin, View):

    def post(self, request):
        obj = get_object_or_404(SocialProfile, pk=request.user.socialprofile.id)
        image = request.FILES['profile_image']
        obj.profile_img = image
        obj.save()
        return HttpResponseRedirect(reverse('profile:profile_update', args=(obj.id,)))


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, profile_id):
        obj = get_object_or_404(SocialProfile, pk=profile_id)
        image_form = ProfileImageForm
        return render(request, 'social_profile/profile_update_form.html', {
            'image_form': image_form,
            'obj': obj,
        })

    def post(self, request, profile_id):
        pass


class RegistrationView(View):
    def get(self, request):
        form = RegistrationForm
        return render(request, 'registration/registration.html', {
            'form': form
        })

    @transaction.atomic
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            profile_user = User.objects.create_user(
                request.POST['username'],
                request.POST['email'],
                request.POST['password']
            )

            profile = SocialProfile(
                user=profile_user,
                last_name=request.POST['last_name'],
                first_name=request.POST['first_name'],
                email=request.POST['email']
            )

            profile.save()
            return HttpResponseRedirect(reverse('institution:search'))
        else:
            return render(request, 'registration/registration.html', {'form': form})


class EducationAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = EducationWithInfoForm
        return render(request, 'social_profile/update/education.html', {'form': form})

    def post(self, request):
        form = EducationWithInfoForm(request.POST)
        if form.is_valid():
            educ = form.save(commit=False)
            educ.profile = request.user.socialprofile
            educ.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)


class WorkExperienceAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = WorkExperienceForm
        return render(request, 'social_profile/update/work_experience.html', {'form': form})

    def post(self, request):
        form = WorkExperienceForm(request.POST)
        if form.is_valid():
            w_e = form.save()
            w_e.socialprofile_set.add(request.user.socialprofile)
            w_e.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)


class InterestAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = InterestForm
        return render(request, 'social_profile/update/interest.html', {'form': form})

    def post(self, request):
        form = InterestForm(request.POST)
        if form.is_valid():
            interest = form.save()
            interest.socialprofile_set.add(request.user.socialprofile)
            interest.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)


class SkillAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = SkillForm
        return render(request, 'social_profile/update/skill.html', {'form': form})

    def post(self, request):
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save()
            skill.socialprofile_set.add(request.user.socialprofile)
            skill.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)


class LanguageAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = LanguageWithLevelForm
        return render(request, 'social_profile/update/language_with_level.html', {'form': form})

    def post(self, request):
        form = LanguageWithLevelForm(request.POST)
        if form.is_valid():
            lang = form.save(commit=False)
            lang.profile = request.user.socialprofile
            lang.save()
            return JsonResponse({'': ''}, safe=False)
        else:
            error_message = "Заполните правильно форму!"
            return JsonResponse({'error': error_message}, safe=False)


def personal_data_update(request, profile_id):
    if request.method == 'POST':
        obj = get_object_or_404(SocialProfile, pk=profile_id)
        form = PersonalDataForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'last_name': request.POST['last_name'],
                                 'first_name': request.POST['first_name'],
                                 'email': request.POST['email'],
                                 'contact_information_phone': request.POST['contact_information_phone'],
                                 'contact_information_address': request.POST['contact_information_address'],
                                 'date_of_birth': request.POST['date_of_birth'],
                                 'patronymic': request.POST['patronymic'],
                                 'about_myself': request.POST['about_myself'],
                                 }, safe=False)
        else:
            return JsonResponse({'': ''}, safe=False)
    else:
        obj = get_object_or_404(SocialProfile, pk=profile_id)
        personal_data_form = PersonalDataForm(instance=obj)
        return render(request, 'social_profile/update/personal_data.html', {
            'form': personal_data_form,
            'obj': obj
        })


def educationWithInfoDelete(request, education_id):
    if request.method == 'POST':
        ed_with_info = get_object_or_404(EducationWithInfo, pk=education_id)
        ed_with_info.delete()
        return JsonResponse({'': ''}, safe=False)
    else:
        pass


def languageWithLevelDelete(request, lang_id):
    if request.method == 'POST':
        lang = get_object_or_404(LanguageWithLevel, pk=lang_id)
        lang.delete()
        return JsonResponse({'': ''}, safe=False)
    else:
        pass


def workExperienceDelete(request, w_e_id):
    if request.method == 'POST':
        w_e = get_object_or_404(WorkExperience, pk=w_e_id)
        w_e.delete()
        return JsonResponse({'': ''}, safe=False)
    else:
        pass