from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET


@require_GET
@cache_control(max_age=86400, public=True)
def robots_txt(request):
    lines = [
        "User-agent: *",
        f"Disallow: /{settings.ADMIN_URL}",
        "Disallow: /ckeditor/",
        "Disallow: /i18n/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
        "",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
@cache_control(max_age=3600, public=True)
def favicon(request):
    from django.shortcuts import redirect
    from django.templatetags.static import static

    # Temporary redirect: the target's hashed name changes whenever the icon
    # does, so browsers must not remember this redirect forever.
    return redirect(static("img/favicon.svg"))
