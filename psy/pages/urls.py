from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),       # Главная страница
    path('blog/', views.blog, name='blog'),  # Блог
]
