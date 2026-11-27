from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render

from portfolio.models import Project
from prices.models import Price
from products.models import Product
from services.models import Service, UsedSystem

from common.forms import rate_limited
from common.i18n import get_site_text

from .forms import ContactForm
from .models import AboutPage, ContactMessage, Founder, HeroSlide, Testimonial, WhyChooseUs


def home(request):
    testimonials = list(Testimonial.objects.filter(is_active=True))
    testimonial_groups = [testimonials[i : i + 4] for i in range(0, len(testimonials), 4)]

    context = {
        "hero_slides": HeroSlide.objects.filter(is_active=True),
        "services": Service.objects.filter(is_active=True).prefetch_related("gallery")[:4],
        "projects": Project.objects.filter(is_active=True)[:3],
        "products": Product.objects.filter(is_active=True).prefetch_related("gallery")[:4],
        "prices": Price.objects.filter(is_active=True)
        .filter(Q(service__isnull=True) | Q(service__is_active=True))
        .select_related("service")[:6],
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
            if form.is_spam():
                # Pretend it worked so bots don't learn to adapt.
                messages.success(request, get_site_text("contact.success"))
                return redirect("contact")
            if rate_limited(request, "contact"):
                messages.error(request, get_site_text("form.too_many"))
                return redirect("contact")
            ContactMessage.objects.create(**form.submission_data())
            messages.success(request, get_site_text("contact.success"))
            return redirect("contact")
    else:
        form = ContactForm(initial={"message": _plan_message(request.GET.get("plan"))})
    return render(request, "core/contact.html", {"form": form})


def _plan_message(plan_id):
    """Pre-fill the message when the visitor came from a pricing card's button."""
    import uuid

    from common.i18n import get_translated

    try:
        price = Price.objects.select_related("service").get(pk=uuid.UUID(str(plan_id)), is_active=True)
    except (ValueError, Price.DoesNotExist):
        return ""
    name = get_translated(price, "price_type_label")
    if price.service:
        name = f"{name} — {get_translated(price.service, 'title')}"
    return f"{get_site_text('pricing.plan_interest')} {name}\n"
