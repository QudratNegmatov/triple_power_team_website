from django.contrib import messages
from django.shortcuts import redirect, render

from portfolio.models import Project
from services.models import Service, UsedSystem

from .forms import ContactForm
from .models import AboutPage, ContactMessage, Founder, HeroSlide, Testimonial, WhyChooseUs


def home(request):
    testimonials = list(Testimonial.objects.filter(is_active=True)[:6])
    testimonial_groups = [testimonials[i : i + 3] for i in range(0, len(testimonials), 3)]

    context = {
        "hero_slides": HeroSlide.objects.filter(is_active=True),
        "services": Service.objects.filter(is_active=True)[:4],
        "projects": Project.objects.filter(is_active=True)[:3],
        "why_us": WhyChooseUs.objects.filter(is_active=True)
        .prefetch_related("points", "stats")
        .first(),
        "about_page": AboutPage.objects.filter(is_active=True).first(),
        "testimonial_groups": testimonial_groups,
        "used_systems": UsedSystem.objects.filter(is_active=True).select_related("service")[:8],
    }
    return render(request, "core/home.html", context)


def about(request):
    about_page = AboutPage.objects.filter(is_active=True).first()
    founders = Founder.objects.filter(is_active=True)
    return render(request, "core/about.html", {"about_page": about_page, "founders": founders})


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
