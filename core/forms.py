from django import forms

from common.forms import SpamProtectedForm


class ContactForm(SpamProtectedForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea, max_length=3000)

    field_order = ["name", "email", "message", "website", "ts"]
