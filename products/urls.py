from django.urls import path

from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    # Old UUID addresses (already shared or indexed) redirect to the slug address.
    path("<uuid:pk>/", views.product_detail_by_id, name="product_detail_by_id"),
    path("<slug:slug>/", views.product_detail, name="product_detail"),
]
