import helpers.numbers
from django.shortcuts import render
from django.db import connection

# Create your views here.
from dashboard.views import dashboard_view

from visits.models import PageVisit

def landing_dashboard_page_view(request):
    print(connection.schema_name)
    if request.user.is_authenticated:
        return dashboard_view(request)
    qs = PageVisit.objects.all()
    PageVisit.objects.create(path=request.path)
    page_views_formatted = helpers.numbers.shorten_number(qs.count() * 100_000)
    social_views_formatted = helpers.numbers.shorten_number(qs.count() * 23_000)
    return render(request, "landing/main.html", {"page_view_count": page_views_formatted, "social_views_count": social_views_formatted})