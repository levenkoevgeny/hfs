from django.urls import path
from . import views

app_name = 'hr'

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('profiles/', views.ProfilesView.as_view(), name='profiles'),
]