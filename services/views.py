from django.shortcuts import get_object_or_404, redirect, render

from .models import Service


def service_list(request):
    return render(
        request,
        "services/service_list.html",
        {"services": Service.objects.filter(is_active=True).prefetch_related("gallery")},
    )


def service_detail_by_id(request, pk):
    obj = get_object_or_404(Service, pk=pk, is_active=True)
    return redirect(obj, permanent=True)


def service_detail(request, slug):
    service = get_object_or_404(Service.objects.prefetch_related("gallery"), slug=slug, is_active=True)
    other_services = Service.objects.filter(is_active=True).exclude(pk=service.pk).prefetch_related("gallery")[:3]
    return render(
        request,
        "services/service_detail.html",
        {
            "service": service,
            "prices": service.prices.filter(is_active=True),
            "used_systems": service.used_systems.filter(is_active=True),
            "integrated_systems": service.integrated_systems.filter(is_active=True),
            "other_services": other_services,
        },
    )
