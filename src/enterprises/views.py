from django.http import HttpResponse
# Create your views here.
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        print(request.user.first_name)
    return HttpResponse(f"your subdomain is {request.tenant_active}")