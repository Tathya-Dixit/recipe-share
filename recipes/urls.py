from django.urls import path
from recipes import views

urlpatterns = [
    path('', views.homeView, name = 'home_page'),
    path('recipes/<int:recipe_id>/', views.recipeDetailView, name = 'recipe_detail'),
    path('recipes/<int:recipe_id>/review/', views.addReviewView, name = 'add_review'),
    path('recipes/<int:recipe_id>/review/delete/', views.deleteReviewView, name = 'delete_review'),
    
]
