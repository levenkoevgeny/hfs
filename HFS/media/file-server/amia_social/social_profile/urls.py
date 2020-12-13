from django.urls import path
from . import views

app_name = 'profile'

urlpatterns = [
    path('<profile_id>/', views.ProfileView.as_view(), name='profile_data'),
    path('new/registration/', views.RegistrationView.as_view(), name='profile_registration'),
    path('update/<int:profile_id>/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('update/personal_data/<profile_id>/', views.personal_data_update, name='profile_update_personal_data'),
    path('education/add/', views.EducationAddView.as_view(), name='profile_education_add'),
    path('education/delete/<education_id>/', views.educationWithInfoDelete, name='profile_education_delete'),
    path('work_experience/add/', views.WorkExperienceAddView.as_view(), name='profile_work_experience_add'),
    path('work_experience/delete/<w_e_id>/', views.workExperienceDelete, name='profile_work_experience_delete'),
    path('interest/add/', views.InterestAddView.as_view(), name='profile_interest_add'),
    path('skill/add/', views.SkillAddView.as_view(), name='profile_skill_add'),
    path('language/add/', views.LanguageAddView.as_view(), name='profile_language_add'),
    path('language/delete/<lang_id>/', views.languageWithLevelDelete, name='profile_language_delete'),
    path('image/update/', views.ProfileImageUpdateView.as_view(), name='profile_image_update'),
]