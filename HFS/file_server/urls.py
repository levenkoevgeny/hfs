from django.urls import path
from . import views

app_name = 'file-server'

urlpatterns = [
    path('', views.index_path),

    path('<path1>/', views.index_path),
    path('<path1>/<path2>/', views.index_path),
    path('<path1>/<path2>/', views.index_path),
    path('<path1>/<path2>/<path3>/', views.index_path),
    path('<path1>/<path2>/<path3>/<path4>/', views.index_path),
    path('<path1>/<path2>/<path3>/<path4>/<path5>/', views.index_path),
    path('<path1>/<path2>/<path3>/<path4>/<path5>/<path6>/', views.index_path),
]