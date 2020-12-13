from django.forms import ModelForm
from .models import SocialProfile, Skill, Interest, WorkExperience, EducationWithInfo, LanguageWithLevel
from django.contrib.auth.models import User
from django import forms

myDateInput = forms.DateInput(format=('%Y-%m-%d'), attrs={'type':'date'})


class RegistrationForm(ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }


# class ProfileForm(ModelForm):
#
#     class Meta:
#         model = SocialProfile
#         exclude = ['user', 'status', 'date_added', 'education', 'work_experience', 'languages', ]
#         widgets = {
#             'date_of_birth': myDateInput
#         }


class ProfileImageForm(ModelForm):

    class Meta:
        model = SocialProfile
        fields = ['profile_img', ]


class PersonalDataForm(ModelForm):

    class Meta:
        model = SocialProfile
        fields = ['last_name', 'first_name',
                  'patronymic', 'email', 'date_of_birth',
                  'about_myself', 'contact_information_phone',
                  'contact_information_address']
        widgets = {
            'date_of_birth': myDateInput
        }


class SkillForm(ModelForm):

    class Meta:
        model = Skill
        fields = '__all__'


class InterestForm(ModelForm):

    class Meta:
        model = Interest
        fields = '__all__'


class WorkExperienceForm(ModelForm):

    class Meta:
        model = WorkExperience
        fields = '__all__'


class EducationWithInfoForm(ModelForm):

    class Meta:
        model = EducationWithInfo
        exclude = ['profile', ]


class LanguageWithLevelForm(ModelForm):

    class Meta:
        model = LanguageWithLevel
        fields = ['language', 'level', ]

