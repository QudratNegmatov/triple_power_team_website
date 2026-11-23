from django.conf import settings

# Pages only load our own scripts and styles. Images and videos may come from
# Cloudinary/S3 or from links pasted into the rich-text editor, so any HTTPS
# host is allowed for media. YouTube/Vimeo may be embedded in articles.
CONTENT_SECURITY_POLICY = "; ".join(
    [
        "default-src 'self'",
        "script-src 'self'",
        "style-src 'self' 'unsafe-inline'",
        "img-src 'self' data: https:",
        "media-src 'self' https:",
        "font-src 'self' data:",
        "connect-src 'self'",
        "frame-src https://www.youtube.com https://www.youtube-nocookie.com https://player.vimeo.com https://www.google.com",
        "object-src 'none'",
        "base-uri 'self'",
        "form-action 'self'",
        "frame-ancestors 'none'",
    ]
)

PERMISSIONS_POLICY = "camera=(), microphone=(), geolocation=(), payment=(), usb=()"


class SecurityHeadersMiddleware:
    """Adds Content-Security-Policy and Permissions-Policy to visitor pages.
    The admin and the CKEditor uploader are left alone (they use inline scripts)."""

    def __init__(self, get_response):
        self.get_response = get_response
        self.skip_prefixes = (f"/{settings.ADMIN_URL}", "/ckeditor/")

    def __call__(self, request):
        response = self.get_response(request)
        response.setdefault("Permissions-Policy", PERMISSIONS_POLICY)
        if not request.path.startswith(self.skip_prefixes):
            response.setdefault("Content-Security-Policy", CONTENT_SECURITY_POLICY)
        return response


LOGIN_FAIL_LIMIT = 8
LOGIN_FAIL_WINDOW = 900  # 15 minutes


def _login_fail_key(request):
    from common.forms import client_ip

    return f"admin-login-fail:{client_ip(request)}"


class AdminLoginThrottleMiddleware:
    """After 8 wrong admin passwords from one IP, refuse further login
    attempts from it for 15 minutes (slows down password guessing)."""

    def __init__(self, get_response):
        from django.contrib.auth.signals import user_login_failed

        self.get_response = get_response
        self.login_path = f"/{settings.ADMIN_URL}login/"
        user_login_failed.connect(self._on_failure, dispatch_uid="admin-login-throttle")

    @staticmethod
    def _on_failure(sender, credentials=None, request=None, **kwargs):
        from django.core.cache import cache

        if request is None:
            return
        key = _login_fail_key(request)
        cache.set(key, cache.get(key, 0) + 1, LOGIN_FAIL_WINDOW)

    def __call__(self, request):
        if request.method == "POST" and request.path == self.login_path:
            from django.core.cache import cache
            from django.http import HttpResponse

            if cache.get(_login_fail_key(request), 0) >= LOGIN_FAIL_LIMIT:
                return HttpResponse(
                    "Too many failed login attempts. Try again in 15 minutes.",
                    status=429,
                    content_type="text/plain",
                )
        return self.get_response(request)
