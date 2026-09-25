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
