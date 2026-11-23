from django import forms

from common.forms import SpamProtectedForm


class ProductInquiryForm(SpamProtectedForm):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=30, required=False)
    message = forms.CharField(widget=forms.Textarea, required=False, max_length=3000)

    field_order = ["name", "email", "phone", "message", "website", "ts"]
