from django.urls import path

from . import views

urlpatterns = [
    path("", views.news_list, name="news_list"),
    # Old UUID addresses (already shared or indexed) redirect to the slug address.
    path("<uuid:pk>/", views.news_detail_by_id, name="news_detail_by_id"),
    path("<slug:slug>/", views.news_detail, name="news_detail"),
]
