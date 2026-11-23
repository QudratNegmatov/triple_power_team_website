from django import forms

from common.i18n import get_site_text


class ProductInquiryForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels come from SiteText ("form.name", ...) so they follow the
        # visitor's language and can be edited in the admin.
        for name, field in self.fields.items():
            field.label = get_site_text(f"form.{name}")
