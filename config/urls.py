from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("products/", include("products.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("news/", include("news.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
