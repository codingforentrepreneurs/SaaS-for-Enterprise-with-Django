from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from django.contrib.auth import get_user_model

from helpers.db.schemas import (
    use_tenant_schema
)

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
    # public schema -> update urls.py -> django-hosts
    owner = request.user
    instance = get_object_or_404(Tenant, owner=owner, pk=pk)
    enterprise_users = []
    with use_tenant_schema(instance.schema_name, create_if_missing=True, revert_public=True):
        # cache?? -> per tenant caching system setup too
        enterprise_users = list(User.objects.all())
    context = {
        "object": instance,
        "instance": instance,
        "enterprise_users": enterprise_users
    }
    return render(request, "tenants/detail.html", context)
