import uuid

from django.conf import settings
from django.db import models


class ContentModel(models.Model):
    """Base for admin-managed content: UUID id, active flag, audit fields.

    Not used for visitor-submitted records (forms) — created_by there would
    always be null, since the submitter isn't an authenticated staff user.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        editable=False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SubmissionModel(models.Model):
    """Base for visitor-submitted records: UUID id + timestamp only."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class SiteText(models.Model):
    """A single piece of static UI copy (nav labels, button text, headings, …),
    editable from the admin without touching templates. Looked up by `key`
    from the {% st "key" %} template tag.
    """

    key = models.SlugField(max_length=100, unique=True, help_text='e.g. "nav.home", "btn.learn_more"')
    description = models.CharField(
        max_length=200, blank=True, help_text="Where this text appears, for whoever edits it later."
    )
    value_en = models.CharField(max_length=500)
    value_uz = models.CharField(max_length=500)
    value_ru = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Site text"
        verbose_name_plural = "Site texts"
        ordering = ["key"]

    def __str__(self):
        return self.key

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        from django.core.cache import cache

        cache.delete("site_text_all")

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        from django.core.cache import cache

        cache.delete("site_text_all")
