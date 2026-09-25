from django.contrib import messages
from django.shortcuts import redirect, render

from portfolio.models import Project
from services.models import Service

from .forms import ContactForm
from .models import ContactMessage, WhyChooseUs


def home(request):
    context = {
        "services": Service.objects.all()[:4],
        "projects": Project.objects.all()[:3],
        "why_us": WhyChooseUs.objects.prefetch_related("points", "stats").first(),
    }
    return render(request, "core/home.html", context)


def about(request):
    return render(request, "core/about.html")


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            ContactMessage.objects.create(**form.cleaned_data)
            messages.success(request, "Thanks for reaching out! We'll get back to you soon.")
            return redirect("contact")
    else:
        form = ContactForm()
    return render(request, "core/contact.html", {"form": form})
