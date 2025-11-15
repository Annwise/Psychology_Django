from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='pages/password_reset.html',
        email_template_name='pages/password_reset_email.html',
        subject_template_name='pages/password_reset_subject.txt'
    ), name='password_reset'),

    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='pages/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='pages/password_reset_confirm.html'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='pages/password_reset_complete.html'
    ), name='password_reset_complete'),

    path('', views.home, name='home'),       # Главная страница
    path('booking/', views.booking_form, name='booking'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('consent/', views.consent_form, name='consent'),
    path('profile/', views.user_profile, name='user_profile'),
    path('admin-bookings/', views.admin_bookings, name='admin_bookings'),

]
