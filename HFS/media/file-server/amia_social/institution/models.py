from django.db import models
from django.contrib.auth.models import User
from social_profile.models import SocialProfile, Language, LanguageLevel, Skill

from .tasks import send_email


class Institution(models.Model):
    institution_name = models.CharField(max_length=255, verbose_name="Institution name")
    info_about = models.TextField(verbose_name="About", blank=True, null=True)
    img = models.ImageField(verbose_name="Image", blank=True, null=True, upload_to='institutions')
    subscribers = models.ManyToManyField(SocialProfile, verbose_name="Subscribers")

    def __str__(self):
        return self.institution_name

    class Meta:
        ordering = ('institution_name',)
        verbose_name = 'Institution'
        verbose_name_plural = 'Institution'


class Vacancy(models.Model):
    OPENED = 1
    COMPLETED = 2
    BLOCKED = 3

    STATUSES = [
        (OPENED, 'Opened'),
        (COMPLETED, 'Completed'),
        (BLOCKED, 'Blocked'),
    ]
    vacancy = models.CharField(max_length=255, verbose_name="Vacancy")
    date_added = models.DateTimeField(verbose_name="Date added", auto_now_add=True)
    who_added = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Who added", blank=True, null=True)
    description = models.TextField(verbose_name="Description", blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, verbose_name="Institution")
    responded = models.ManyToManyField(SocialProfile, verbose_name="Responded", through='RespondedVacancy')
    status = models.IntegerField(verbose_name="Status", choices=STATUSES, default=OPENED)
    skills = models.ManyToManyField(Skill, verbose_name="Skills", blank=True)
    languages = models.ManyToManyField(Language, verbose_name="Language", through='LanguageWithLevelVacancy')

    def __str__(self):
        return self.vacancy + ' ' + self.institution.institution_name

    class Meta:
        ordering = ('vacancy',)
        verbose_name = 'Vacancy'
        verbose_name_plural = 'Vacancies'

    def save(self, *args, **kwargs):
        if self.pk:
            created = False
        else:
            created = True
        super().save(*args, **kwargs)
        # send_email.delay(self.institution.pk, self.pk, created)


class RespondedVacancy(models.Model):
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    date_of_response = models.DateTimeField(verbose_name="Date of response", auto_now_add=True)


class LanguageWithLevelVacancy(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE)
    level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.language.language_name + ' ' + self.vacancy.vacancy + ' ' + str(self.level.language_level)