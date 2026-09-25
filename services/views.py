from django.shortcuts import get_object_or_404, render

from .models import Service


def service_list(request):
    return render(
        request,
        "services/service_list.html",
        {"services": Service.objects.filter(is_active=True)},
    )


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "prices": service.prices.filter(is_active=True),
            "other_services": other_services,
        },
    )
