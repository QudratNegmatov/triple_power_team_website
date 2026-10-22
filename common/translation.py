"""Machine translation for admin forms: English -> Uzbek / Russian.

Used by the "Translate" button on admin change forms. Nothing is saved here -
the translations are sent back to the form so an editor can review and fix
them before clicking Save.
"""

import json
import os

import anthropic

TARGET_LANGUAGES = {"uz": "Uzbek (Latin script)", "ru": "Russian"}

SYSTEM_PROMPT = """\
You translate website copy for Triple Power Team, a US trucking services company \
(ELD / hours-of-service compliance, dispatch, safety and fleet services for trucking \
companies and owner-operators). The source text is English. Translate each field into \
Uzbek (Latin script) and Russian.

Rules:
- Keep the meaning exactly. Do not add, drop or soften any claim, number or promise.
- Write natural, professional copy a native speaker in the trucking business would write - \
not a word-for-word translation.
- Uzbek: Latin script, using the apostrophe ' in o', g' and as the tutuq belgisi (e.g. \
"ko'rsatish", "ma'lumot"). Trucking slang used by Uzbek drivers is fine where it reads \
naturally: "truck", "driver", "dispatch", "broker", "yuk".
- Russian: use the industry terms Russian-speaking US truckers use: "трак", "брокер", \
"диспетчер", "груз", "водитель".
- Never translate: brand and product names (Triple Power Team, PandaELD, UzbPrime ELD, \
BST ELD, Vitality ELD, Highway, Trucking Tools, Amazon Relay, etc.), acronyms (ELD, HOS, \
DOT, FMCSA, IFTA, CSA, IRP, BOL, POD, DQ), URLs, e-mail addresses, phone numbers.
- Keep numbers, units and symbols as they are (2000+, 24/7, $149.00, 99%).
- If a field is HTML, translate only the visible text and keep every tag and attribute \
exactly as in the source.
- Keep line breaks: a field with one item per line must come back with the same number of \
lines, in the same order.
- If a field has a max length, the translation must fit within it; shorten wording if needed \
without losing meaning.
- Return every field you were given, matched by its "key".
"""

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "translations": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "key": {"type": "string"},
                    "uz": {"type": "string"},
                    "ru": {"type": "string"},
                },
                "required": ["key", "uz", "ru"],
                "additionalProperties": False,
            },
        }
    },
    "required": ["translations"],
    "additionalProperties": False,
}


class TranslationError(Exception):
    """A user-facing error message for the admin UI."""


def translate_fields(fields):
    """Translate a list of {"key", "text", "html", "max_length"} dicts.

    Returns {key: {"uz": ..., "ru": ...}}.
    """
    if not fields:
        return {}
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise TranslationError(
            "Translation is not set up: add the ANTHROPIC_API_KEY environment variable on the server."
        )

    payload = [
        {
            "key": f["key"],
            "format": "html" if f.get("html") else "plain text",
            **({"max_length": f["max_length"]} if f.get("max_length") else {}),
            "text": f["text"],
        }
        for f in fields
    ]

    client = anthropic.Anthropic()
    try:
        response = client.beta.messages.create(
            model=os.environ.get("TRANSLATION_MODEL", "claude-opus-5-5"),
            max_tokens=32000,
            system=SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": "Translate these fields:\n\n" + json.dumps(payload, ensure_ascii=False, indent=1),
                }
            ],
            output_config={"effort": "medium", "format": {"type": "json_schema", "schema": OUTPUT_SCHEMA}},
            # If a safety classifier declines the request, retry it server-side on
            # Anthropic's recommended fallback model instead of failing.
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
        )
    except anthropic.AuthenticationError:
        raise TranslationError("Translation failed: the ANTHROPIC_API_KEY is invalid.")
    except anthropic.RateLimitError:
        raise TranslationError("Translation service is busy - try again in a minute.")
    except anthropic.APIConnectionError:
        raise TranslationError("Could not reach the translation service - check the server's internet access.")
    except anthropic.APIStatusError as e:
        raise TranslationError(f"Translation failed ({e.status_code}): {e.message}")

    if response.stop_reason == "refusal":
        raise TranslationError("The translation service declined this text.")
    if response.stop_reason == "max_tokens":
        raise TranslationError("The text is too long to translate in one go - translate fewer fields at a time.")

    text = next((b.text for b in response.content if b.type == "text"), "")
    try:
        items = json.loads(text)["translations"]
    except (ValueError, KeyError):
        raise TranslationError("The translation service returned an unexpected response - try again.")

    wanted = {f["key"] for f in fields}
    return {item["key"]: {"uz": item["uz"], "ru": item["ru"]} for item in items if item["key"] in wanted}
