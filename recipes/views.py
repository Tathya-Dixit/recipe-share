from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from recipes.models import Recipe, Review

def homeView(request):
    recipes = Recipe.objects.all()
    context = {
        'recipes': recipes,
        'total_recipes': recipes.count(),
    }
    return render(request, 'recipes/home.html', context)

def recipeDetailView(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    reviews = recipe.reviews.all()

    curr_user_reviewed = False
    if request.user.is_authenticated:
        curr_user_reviewed = reviews.filter(reviewer = request.user).exists()
    
    context = {
        'recipe': recipe,
        'reviews': reviews,
        'curr_user_reviewed': curr_user_reviewed,
        'average_rating': recipe.average_rating(),
        'total_reviews': reviews.count()
    }

    return render(request, 'recipes/recipe_detail.html', context)

@login_required
def addReviewView(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)
    
    if request.method == 'POST':
        if request.user == recipe.author:
            messages.error(request, 'You can not review your own recipe!')
            return redirect('recipe_detail', recipe_id = recipe_id)
    
        if Review.objects.filter(recipe = recipe, reviewer = request.user).exists():
            messages.error(request, "You've already reviewed for this recipe.Now you can either edit it or delete it.")
            return redirect('recipe_detail', recipe_id = recipe_id)
        
        rating = request.POST.get('rating')
        review = request.POST.get('review', '').strip()

        if not rating:
            messages.error(request, 'Please select rating before submission!')
            return redirect('recipe_detail', recipe_id = recipe_id)

        Review.objects.create(
            review = review,
            rating = rating,
            reviewer = request.user,
            recipe = recipe
        )
    
        messages.success(request, 'Added Review Successfully!')
    
    return redirect('recipe_detail', recipe_id = recipe_id)


@login_required
def deleteReviewView(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)

    try:
        review = Review.objects.get(recipe = recipe, reviewer = request.user)
        review.delete()
        messages.success(request, 'Review Deletd Successfully!')
    except Review.DoesNotExist:
        messages.error(request, 'Review not found!')
    
    return redirect('recipe_detail', recipe_id = recipe_id)
    
