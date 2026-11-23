from django import forms

from common.i18n import get_site_text


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Labels come from SiteText ("form.name", ...) so they follow the
        # visitor's language and can be edited in the admin.
        for name, field in self.fields.items():
            field.label = get_site_text(f"form.{name}")
