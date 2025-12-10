from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.homeView, name = 'home_page')
]
