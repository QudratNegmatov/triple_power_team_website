from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductInquiryForm
from .models import Product, ProductInquiry


def product_list(request):
    products = Product.objects.filter(is_active=True)
    return render(request, "products/product_list.html", {"products": products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    if request.method == "POST":
        form = ProductInquiryForm(request.POST)
        if form.is_valid():
            ProductInquiry.objects.create(product=product, **form.cleaned_data)
            messages.success(request, "Thanks! We received your request and will contact you soon.")
            return redirect("product_detail", pk=product.pk)
    else:
        form = ProductInquiryForm()
    other_products = Product.objects.filter(is_active=True).exclude(pk=pk)[:3]
    return render(
        request,
        "products/product_detail.html",
        {"product": product, "form": form, "other_products": other_products},
    )
