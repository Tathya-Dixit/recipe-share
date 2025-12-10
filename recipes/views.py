from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def homeView(request):
    return render(request, 'recipes/home.html')
