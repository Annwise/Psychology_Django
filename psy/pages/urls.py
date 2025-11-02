from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),       # Главная страница
    path('booking/', views.booking_form, name='booking'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('consent/', views.consent_form, name='consent'),
]
