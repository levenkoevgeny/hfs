from django.urls import path
from . import views

app_name = 'institution'

urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('<institution_id>/vacancy', views.InstitutionVacancyView.as_view(), name='institution_vacancy'),
    path('vacancy/add/', views.VacancyAddView.as_view(), name='vacancy_add'),
    path('vacancy/<vacancy_id>/update/', views.VacancyUpdateView.as_view(), name='vacancy_update'),
    path('vacancy/<pk>/delete/', views.VacancyDelete.as_view(), name='vacancy_delete'),
    path('vacancy/getresponse', views.vacancy_response, name='get_vacancy_response'),
    path('getsubscription', views.subscription, name='get_subscription')
]
