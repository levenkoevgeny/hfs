from django.forms import ModelForm
from .models import Vacancy, LanguageWithLevelVacancy


class VacancyForm(ModelForm):

    class Meta:

        model = Vacancy
        fields = ['institution', 'vacancy', 'who_added', 'description', 'status', 'skills']


class LanguageWithLevelVacancyForm(ModelForm):

    class Meta:

        model = LanguageWithLevelVacancy
        fields = ['language', 'level']