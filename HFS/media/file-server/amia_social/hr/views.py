from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

from institution.models import Vacancy

from social_profile.models import SocialProfile
from .filters import VacancyFilter, ProfileFilter
from django.core.paginator import Paginator


class MainView(LoginRequiredMixin, View):

    def get(self, request):
        f = VacancyFilter(request.GET, queryset=Vacancy.objects.distinct().order_by('-pk'))
        paginator = Paginator(f.qs, 50)
        page = request.GET.get('page')
        vacancies = paginator.get_page(page)
        return render(request, 'institution/vacancies/hr_main_vacancies.html', {'vacancies': vacancies,
                                                                                'filter': f,
                                                                                })


class ProfilesView(LoginRequiredMixin, View):

    def get(self, request):
        f = ProfileFilter(request.GET, queryset=SocialProfile.objects.exclude(user=request.user).distinct().order_by('-pk'))
        paginator = Paginator(f.qs, 50)
        page = request.GET.get('page')
        profiles = paginator.get_page(page)
        return render(request, 'hr/profiles/profiles.html', {'profiles': profiles,
                                                             'filter': f,
                                                             })
