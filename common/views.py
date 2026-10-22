import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .translation import TranslationError, translate_fields

MAX_FIELDS = 200


@staff_member_required
@require_POST
def admin_translate(request):
    """Translate the English fields of an admin form into Uzbek and Russian.

    Expects {"fields": [{"key", "text", "html", "max_length"}, ...]} and returns
    {"translations": {key: {"uz": ..., "ru": ...}}}. Nothing is saved.
    """
    try:
        fields = json.loads(request.body)["fields"]
        fields = [
            {
                "key": str(f["key"]),
                "text": str(f["text"]),
                "html": bool(f.get("html")),
                "max_length": int(f["max_length"]) if f.get("max_length") else None,
            }
            for f in fields
            if str(f.get("text", "")).strip()
        ]
    except (ValueError, KeyError, TypeError):
        return JsonResponse({"error": "Bad request."}, status=400)
    if len(fields) > MAX_FIELDS:
        return JsonResponse({"error": f"Too many fields (max {MAX_FIELDS})."}, status=400)

    try:
        translations = translate_fields(fields)
    except TranslationError as e:
        return JsonResponse({"error": str(e)}, status=502)
    return JsonResponse({"translations": translations})
