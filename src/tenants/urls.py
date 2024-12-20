
from django.urls import path

from . import views

urlpatterns = [
    path("", views.tenant_list_view),
    path("<str:pk>/", views.tenant_detail_view),
]
