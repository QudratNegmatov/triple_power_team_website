from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from common.forms import rate_limited
from common.i18n import get_site_text

from .forms import ProductInquiryForm
from .models import Product, ProductInquiry


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "products/product_list.html", {"products": products})


def product_detail_by_id(request, pk):
    obj = get_object_or_404(Product, pk=pk, is_active=True)
    return redirect(obj, permanent=True)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related("gallery"), slug=slug, is_active=True)
    if request.method == "POST":
        form = ProductInquiryForm(request.POST)
        if form.is_valid():
            if form.is_spam():
                messages.success(request, get_site_text("products.success"))
                return redirect(product)
            if rate_limited(request, "product"):
                messages.error(request, get_site_text("form.too_many"))
                return redirect(product)
            ProductInquiry.objects.create(product=product, **form.submission_data())
            messages.success(request, get_site_text("products.success"))
            return redirect(product)
    else:
        form = ProductInquiryForm()
    other_products = Product.objects.filter(is_active=True).exclude(pk=product.pk)[:3]
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "form": form, "other_products": other_products},
    )
