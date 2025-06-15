from django.urls import path
from site_psy import views

urlpatterns = [
    path('', views.index, name='home'),
]
