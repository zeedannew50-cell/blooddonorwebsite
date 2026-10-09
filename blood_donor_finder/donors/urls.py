from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('donated/<str:donor_id>/', views.donated, name='donated'),
    path('delete/<str:donor_id>/', views.delete, name='delete'),
]
