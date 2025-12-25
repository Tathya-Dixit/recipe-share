from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import User
from accounts.forms import ProfileForm

def registerView(request):
    if request.user.is_authenticated:
        return redirect('home_page')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords don't match!")
            return render(request, 'accounts/register.html')
        
        if len(password1) < 8:
            messages.error(request, 'Password must be atleast 8 characters long!')
            return render(request, 'accounts/register.html')
        
        if len(username) < 5:
            messages.error(request, 'Username must be atleast 5 characters long!')
            return render(request, 'accounts/register.html')
        
        if User.objects.filter(username = username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email = email).exists():
            messages.error(request, 'Email already registered! Try Forgot Password?')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(
            username = username,
            email = email,
            password = password1
        )        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('login')
    
    return render(request, 'accounts/register.html')        


def loginView(request):
    if request.user.is_authenticated:
        return redirect('home_page')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('home_page')
        else:
            messages.error(request, 'Invaild username or password!')
    
    return render(request, 'accounts/login.html')


def logoutView(request):
    logout(request)
    messages.success(request, 'See you again!')
    return redirect('home_page')


@login_required
def profileView(request):
    user = request.user
    recipes = user.recipes.all()

    context = {
        'user': user,
        'recipes': recipes,
        'total_recipes': recipes.count(),
    }

    return render(request, 'accounts/profile.html', context)


@login_required
def editProfileView(request):
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance = request.user)

        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile Successfully Updated')
            return redirect('profile')
    else:
        profile_form = ProfileForm(instance = request.user)
    
    return render(request, 'accounts/edit_profile.html', {'form' : profile_form})

def publicProfileView(request, username):
    user = get_object_or_404(User, username = username)
    user_recipes = user.recipes.all()

    context = {
        'profile_user': user,
        'recipes': user_recipes,
        'total_recipes': user_recipes.count(),
        'is_own_profile': request.user == user,
    }
    
    return render(request, 'accounts/public_profile.html', context)
