
from django.urls import path, include

from . import views

# enterprises url conf
urlpatterns = [
    path("", views.home_view, name='home'),
    path('accounts/', include('allauth.urls')),
]
