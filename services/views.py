from django.shortcuts import get_object_or_404, render

from .models import Service


def service_list(request):
    return render(request, "services/service_list.html", {"services": Service.objects.all()})


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    other_services = Service.objects.exclude(slug=slug)[:3]
    return render(
        request,
        "services/service_detail.html",
        {"service": service, "other_services": other_services},
    )
