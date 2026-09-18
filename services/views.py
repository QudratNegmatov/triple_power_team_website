from django.shortcuts import render

from .models import Service


def service_list(request):
    return render(request, "services/service_list.html", {"services": Service.objects.all()})
