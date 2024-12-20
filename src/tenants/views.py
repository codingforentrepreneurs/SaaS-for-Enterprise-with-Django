from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.contrib.auth import get_user_model

from .models import Tenant

User = get_user_model()

@login_required
def tenant_list_view(request):
    owner = request.user
    context = {
        "object_list": Tenant.objects.filter(owner=owner)
    }
    return render(request, "tenants/list.html", context)


@login_required
def tenant_detail_view(request, pk):
    owner = request.user
    instance = get_object_or_404(Tenant, owner=owner, pk=pk)
    context = {
        "object": instance,
        "instance": instance,
    }
    return render(request, "tenants/detail.html", context)
