import helpers.numbers
from django.http import HttpResponse
from django.shortcuts import render
from django.db import connection

# Create your views here.
from dashboard.views import dashboard_view

from visits.models import PageVisit

from decouple import config
from helpers.db import use_dynamic_database_url

def landing_dashboard_page_view(request):
    qs = PageVisit.objects.all()
    print("this is working...")
    print(f"og visits, {qs.count()}")
    DB_URL_2 = config('DB_URL_2', default=None)
    if DB_URL_2 is not None:
        alias = 'db_url_2'
        with use_dynamic_database_url(DB_URL_2, alias=alias):
            qs = PageVisit.objects.using(alias).all()
            PageVisit.objects.using(alias).create(path=request.path, user=None)
            print('page visis', qs.count())
    # if not request.tenant_active:
    #     return HttpResponse("invalid subdomain")
    user = None
    if request.user.is_authenticated:
        user = request.user
    PageVisit.objects.create(path=request.path, user=user)
    qs = PageVisit.objects.all()
    print('other qs visits', qs.count())
    if user is not None:
        return dashboard_view(request)
    
    page_views_formatted = helpers.numbers.shorten_number(qs.count() * 100_000)
    social_views_formatted = helpers.numbers.shorten_number(qs.count() * 23_000)
    return render(request, "landing/main.html", {"page_view_count": page_views_formatted, "social_views_count": social_views_formatted})