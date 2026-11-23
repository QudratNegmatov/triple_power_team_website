import time

from django import forms
from django.core import signing
from django.core.cache import cache

from common.i18n import get_site_text

MIN_FILL_SECONDS = 3
RATE_LIMIT = 5  # submissions ...
RATE_WINDOW = 600  # ... per 10 minutes per IP address


class SpamProtectedForm(forms.Form):
    """Blocks most spam bots without a captcha:
    - `website` is a honeypot: hidden from people with CSS, bots fill it in;
    - `ts` is a signed render time: forms sent faster than 3 s are bots;
    Field labels come from SiteText ("form.<name>") in the visitor's language."""

    website = forms.CharField(required=False, label="Website")
    ts = forms.CharField(required=False, widget=forms.HiddenInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["ts"].initial = signing.dumps(int(time.time()), salt="form-ts")
        self.fields["website"].widget.attrs.update({"tabindex": "-1", "autocomplete": "off"})
        autocomplete = {"name": "name", "email": "email", "phone": "tel"}
        for name, field in self.fields.items():
            if name not in ("website", "ts"):
                field.label = get_site_text(f"form.{name}")
            if name in autocomplete:
                field.widget.attrs["autocomplete"] = autocomplete[name]
        if "phone" in self.fields:
            self.fields["phone"].widget.input_type = "tel"

    def is_spam(self):
        if self.cleaned_data.get("website"):
            return True
        try:
            rendered = signing.loads(self.cleaned_data.get("ts") or "", salt="form-ts", max_age=86400)
        except signing.BadSignature:
            return True
        return time.time() - rendered < MIN_FILL_SECONDS

    def submission_data(self):
        return {k: v for k, v in self.cleaned_data.items() if k not in ("website", "ts")}


def client_ip(request):
    return (
        request.META.get("HTTP_CF_CONNECTING_IP")
        or request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
        or request.META.get("REMOTE_ADDR", "")
    )


def rate_limited(request, scope):
    """True when this IP has already sent RATE_LIMIT forms in RATE_WINDOW seconds."""
    key = f"form-rate:{scope}:{client_ip(request)}"
    count = cache.get(key, 0)
    if count >= RATE_LIMIT:
        return True
    cache.set(key, count + 1, RATE_WINDOW)
    return False
