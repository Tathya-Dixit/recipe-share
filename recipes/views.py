from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from recipes.models import Recipe, Review
from recipes.forms import RecipeForm

def homeView(request):
    recipes = Recipe.objects.all()

    search_query = request.GET.get('search', '').strip()
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) | 
            Q(ingredients_list__icontains=search_query)
        )
    
    recipes = recipes.order_by('-created_at')
    
    paginator = Paginator(recipes, 9)
    page_number = request.GET.get('page', 1)

    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'recipes': page_obj,
        'page_obj': page_obj,
        'total_recipes': paginator.count,
        'search_query': search_query,
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


@login_required
def createRecipeView(request):
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit = False)
            recipe.author = request.user
            recipe.save()

            messages.success(request, 'Your Recipe has been successfully submitted. It will be published once it is verified.')#will add verification functionality later on when mvp is working
            return redirect('recipe_detail', recipe_id = recipe.id)
    else:
        recipe_form = RecipeForm()
    
    return render(request, 'recipes/recipe_form.html',{'form': recipe_form})


@login_required
def editRecipeView(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id)

    if request.user != recipe.author:
        messages.error(request, "You shouldn't try to edit someone else's recipe. This is forbidden on this safe platform.")
        return redirect('recipe_detail', recipe_id = recipe_id)
    
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES, instance = recipe)

        if recipe_form.is_valid():
            recipe_form.save()
            messages.success(request, 'Recipe Successfully Edited!')
            return redirect('recipe_detail', recipe_id = recipe_id)
    else:
        recipe_form = RecipeForm(instance = recipe)
    
    context = {
        'form': recipe_form,
        'recipe': recipe,
        'is_edit': True
    }
    return render(request, 'recipes/recipe_form.html', context)


@login_required
def deleteRecipeView(request, recipe_id):
    recipe = get_object_or_404(Recipe, id = recipe_id) 

    if request.user != recipe.author:
        messages.error(request, "You shouldn't try to edit someone else's recipe. This is forbidden on this safe platform.")
        return redirect('recipe_detail', recipe_id = recipe_id)

    if request.method == 'POST':
        recipe.delete()
        messages.success(request, 'Recipe Deleted Successfully!')
        return redirect('home_page')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe' : recipe})



