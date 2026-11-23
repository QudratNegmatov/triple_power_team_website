from django.urls import path

from . import views

urlpatterns = [
    path("", views.service_list, name="service_list"),
    # Old UUID addresses (already shared or indexed) redirect to the slug address.
    path("<uuid:pk>/", views.service_detail_by_id, name="service_detail_by_id"),
    path("<slug:slug>/", views.service_detail, name="service_detail"),
]
