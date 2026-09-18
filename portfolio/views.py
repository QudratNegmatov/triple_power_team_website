from django.shortcuts import render

from .models import Project


def project_list(request):
    return render(request, "portfolio/project_list.html", {"projects": Project.objects.all()})
