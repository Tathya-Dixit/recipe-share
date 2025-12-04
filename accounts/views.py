from django.shortcuts import render

def testView(request):
    return render(request, 'base.html')
