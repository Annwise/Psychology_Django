from django.urls import path
from . import views

urlpatterns = [
    path('', views.blog, name='blog'),
    path('article/<int:article_id>/', views.article, name='article'),
]
