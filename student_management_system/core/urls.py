from django.urls import path
from . import views

urlpatterns = [
    path('', views.study_list, name='study_list'),
    path('add/', views.add_study, name='add_study'),
    path('edit/<int:id>/', views.edit_study, name='edit_study'),
    path('view/<int:id>/', views.view_study, name='view_study'),
    path('delete/<int:id>/', views.delete_study, name='delete_study'),
]
