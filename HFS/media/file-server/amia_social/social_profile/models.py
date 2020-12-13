from django.db import models
from django.contrib.auth.models import User


class Skill(models.Model):
    skill_name = models.CharField(max_length=255, verbose_name="Skill")

    def __str__(self):
        return self.skill_name

    class Meta:
        ordering = ('skill_name',)
        verbose_name = 'Skill'
        verbose_name_plural = 'Skills'


class Interest(models.Model):
    interest_name = models.CharField(max_length=255, verbose_name="Interest")

    def __str__(self):
        return self.interest_name

    class Meta:
        ordering = ('interest_name',)
        verbose_name = 'Interest'
        verbose_name_plural = 'Interests'


class Language(models.Model):
    language_name = models.CharField(max_length=100, verbose_name="Language_name")

    def __str__(self):
        return self.language_name

    class Meta:
        ordering = ('language_name',)
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'


class LanguageLevel(models.Model):
    LEVELS = (
        (1, 'Beginner'),
        (2, 'Pre-Intermediate'),
        (3, 'Intermediate'),
        (4, 'Upper-Intermediate'),
        (5, 'Advanced'),
        (6, 'Proficiency'),
    )
    language_level = models.IntegerField(verbose_name="language_level", choices=LEVELS)

    def __str__(self):
        level_index = int(self.language_level) - 1
        return str(self.LEVELS[level_index][1])

    class Meta:
        ordering = ('language_level',)
        verbose_name = 'Language level'
        verbose_name_plural = 'Language levels'


class EducationalInstitution(models.Model):
    institutional_name = models.CharField(max_length=255, verbose_name="Institutional name")

    def __str__(self):
        return self.institutional_name

    class Meta:
        ordering = ('institutional_name',)
        verbose_name = 'Education'
        verbose_name_plural = 'Educations'


class Specialty(models.Model):
    specialty_name = models.CharField(max_length=255, verbose_name="Specialty name")
    education = models.ForeignKey(EducationalInstitution, on_delete=models.CASCADE, verbose_name="Education")

    def __str__(self):
        return self.specialty_name + ' ' + self.education.institutional_name

    class Meta:
        ordering = ('specialty_name',)
        verbose_name = 'Specialty'
        verbose_name_plural = 'Specialties'


class WorkExperience(models.Model):
    company_name = models.CharField(max_length=255, verbose_name="Company name")
    position = models.CharField(max_length=255, verbose_name="Position")
    duty = models.TextField(verbose_name="Duty", blank=True, null=True)
    year_start = models.IntegerField(verbose_name="Start year")
    year_end = models.IntegerField(verbose_name="End year", blank=True, null=True)

    def __str__(self):
        return self.position + ' ' + self.company_name

    class Meta:
        ordering = ('-year_start',)
        verbose_name = 'Work experience'
        verbose_name_plural = 'Work experience'


class SocialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    last_name = models.CharField(max_length=100, verbose_name="Last name")
    first_name = models.CharField(max_length=100, verbose_name="First name")
    patronymic = models.CharField(max_length=100, verbose_name="Patronymic", blank=True, null=True)
    email = models.EmailField(verbose_name="E-mail")
    date_of_birth = models.DateField(verbose_name="Date_of_birth", blank=True, null=True)
    status = models.IntegerField(verbose_name="Status", default=1)
    date_added = models.DateTimeField(verbose_name="Date_added", auto_now_add=True)
    profile_img = models.ImageField(verbose_name="Profile_img", blank=True, null=True, upload_to='profile')
    about_myself = models.TextField(verbose_name="About_myself", blank=True, null=True)
    contact_information_phone = models.CharField(max_length=255, verbose_name="Phone", blank=True, null=True)
    contact_information_address = models.CharField(max_length=255, verbose_name="Address", blank=True, null=True)
    education = models.ManyToManyField(Specialty, verbose_name="Education", through="EducationWithInfo")
    work_experience = models.ManyToManyField(WorkExperience, verbose_name="Work experience")
    interests = models.ManyToManyField(Interest, verbose_name="Interests", blank=True)
    skills = models.ManyToManyField(Skill, verbose_name="Skills", blank=True)
    languages = models.ManyToManyField(Language, verbose_name="Language", through='LanguageWithLevel')

    def __str__(self):
        return self.last_name

    class Meta:
        ordering = ('last_name',)
        verbose_name = 'Social profile'
        verbose_name_plural = 'Social profiles'
# Many to many through


class LanguageWithLevel(models.Model):
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    level = models.ForeignKey(LanguageLevel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.profile) + ' ' + self.language.language_name + ' ' + str(self.level)


class EducationWithInfo(models.Model):
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE)
    profile = models.ForeignKey(SocialProfile, on_delete=models.CASCADE)
    year_of_entrance = models.IntegerField(verbose_name="Year of entrance")
    year_of_graduating = models.IntegerField(verbose_name="Year of graduating", blank=True, null=True)

    def __str__(self):
        return self.specialty.specialty_name + ' ' + self.profile.last_name