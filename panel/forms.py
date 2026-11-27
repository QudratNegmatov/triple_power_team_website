from django import forms
from django.db import models
from django.forms.models import inlineformset_factory, modelform_factory

from .labels import ICON_CHOICES, LANGUAGES, PERIOD_CHOICES, base_name, help_for, label_for
from .registry import expand

RICH_TEXT_FIELDS = {"full_info", "full_description"}
LONG_TEXT_FIELDS = {"key_points", "features", "body", "feedback", "description", "message"}


class ImageInput(forms.ClearableFileInput):
    template_name = "panel/widgets/image.html"

    def __init__(self, attrs=None):
        super().__init__({"accept": "image/*", **(attrs or {})})


class VideoInput(forms.ClearableFileInput):
    template_name = "panel/widgets/file.html"

    def __init__(self, attrs=None):
        super().__init__({"accept": "video/*", **(attrs or {})})


class RichTextInput(forms.Textarea):
    """A small editor of our own (bold, headings, lists, links); the HTML is
    kept in the textarea that is submitted."""

    template_name = "panel/widgets/richtext.html"


def panel_formfield(db_field, **kwargs):
    name = db_field.name
    base, _lang = base_name(name)

    if base in RICH_TEXT_FIELDS:
        field = forms.CharField(required=not db_field.blank, widget=RichTextInput)
    elif isinstance(db_field, models.ImageField):
        field = db_field.formfield(widget=ImageInput, **kwargs)
    elif isinstance(db_field, models.FileField):
        field = db_field.formfield(widget=VideoInput, **kwargs)
    elif isinstance(db_field, models.DateTimeField):
        field = db_field.formfield(
            widget=forms.DateTimeInput(attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"), **kwargs
        )
    elif name == "icon":
        field = forms.ChoiceField(choices=ICON_CHOICES, required=not db_field.blank)
    elif name == "period":
        field = forms.ChoiceField(choices=PERIOD_CHOICES)
    elif isinstance(db_field, models.TextField) or (
        base == "value" and isinstance(db_field, models.CharField)
    ):
        rows = 6 if base in LONG_TEXT_FIELDS else 3
        field = db_field.formfield(widget=forms.Textarea(attrs={"rows": rows}), **kwargs)
    else:
        field = db_field.formfield(**kwargs)

    if field is None:
        return None
    field.label = label_for(name)
    field.help_text = help_for(name)
    return field


def form_class(resource, editing=False):
    names = [n for n in resource.form_fields() if not (editing and n in resource.readonly_on_edit)]
    names = [n for n in names if n != "created_at"]
    return modelform_factory(resource.model, fields=names, formfield_callback=panel_formfield)


def formset_class(resource, inline):
    return inlineformset_factory(
        resource.model,
        inline.model,
        fields=expand(inline.fields),
        extra=0,
        can_delete=True,
        formfield_callback=panel_formfield,
    )


def rows_for(form, specs):
    """Turn ["title*", "order"] into rows the template draws: a translated row
    holds one bound field per language."""
    rows = []
    for spec in specs:
        if spec.endswith("*"):
            base = spec[:-1]
            if f"{base}_en" not in form.fields:
                continue
            rows.append(
                {
                    "translated": True,
                    "label": label_for(base),
                    "help": help_for(base),
                    "fields": [(code, label, form[f"{base}_{code}"]) for code, label in LANGUAGES],
                }
            )
        elif spec in form.fields:
            rows.append({"translated": False, "field": form[spec]})
    return rows
