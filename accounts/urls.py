from django.urls import path
from accounts.views import testView


urlpatterns = [
    path('', testView)
]
