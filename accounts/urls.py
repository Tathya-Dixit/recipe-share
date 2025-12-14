from django.urls import path
from accounts import views


urlpatterns = [
    path('register/', views.registerView, name = 'register'),
    path('login/', views.loginView, name = 'login'),
    path('logout/', views.logoutView, name = 'logout'),
    path('profile/', views.profileView, name = 'profile'),
    path('profile/edit/', views.editProfileView, name = 'edit_profile'),
]
