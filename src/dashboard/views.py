from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from visits.models import PageVisit

@login_required
def dashboard_view(request):
    qs = PageVisit.objects.all() #.filter(user=request.user)
    visit_count = qs.count()
    return render(request, "dashboard/main.html", {
        "visit_count": visit_count,
    })