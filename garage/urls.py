from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.projects_list, name='projects_list'),
    path('projects/add/', views.project_create, name='project_create'),
    path('api/projects/', views.api_projects_list, name='api_projects_list'),
    path('projects/<int:pk>/edit/', views.project_update, name='project_update'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
]