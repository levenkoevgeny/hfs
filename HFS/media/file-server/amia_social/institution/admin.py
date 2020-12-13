from django.contrib import admin
from .models import Institution, Vacancy, RespondedVacancy, LanguageWithLevelVacancy

admin.site.register(Institution)
admin.site.register(Vacancy)
admin.site.register(RespondedVacancy)
admin.site.register(LanguageWithLevelVacancy)