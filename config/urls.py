from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from common.sitemaps import SITEMAPS
from common.views import favicon, robots_txt

urlpatterns = [
    path(settings.ADMIN_URL, include("panel.urls")),
    path(settings.DJANGO_ADMIN_URL, admin.site.urls),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("favicon.ico", favicon),
    path("sitemap.xml", sitemap, {"sitemaps": SITEMAPS}, name="django.contrib.sitemaps.views.sitemap"),
]

# Every visitor page has its own address per language, so search engines can
# index all three: English at /, Uzbek at /uz/..., Russian at /ru/...
urlpatterns += i18n_patterns(
    path("", include("core.urls")),
    path("services/", include("services.urls")),
    path("products/", include("products.urls")),
    path("portfolio/", include("portfolio.urls")),
    path("news/", include("news.urls")),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
