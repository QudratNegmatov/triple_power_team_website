import json
from types import SimpleNamespace
from unittest import mock

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse

from . import translation


class AdminTranslateViewTests(TestCase):
    def setUp(self):
        self.url = reverse("admin_translate")
        self.staff = get_user_model().objects.create_user("staff", password="pw", is_staff=True)

    def post(self, payload):
        return self.client.post(self.url, json.dumps(payload), content_type="application/json")

    def test_requires_staff(self):
        response = self.post({"fields": []})
        self.assertEqual(response.status_code, 302)  # redirected to admin login

    def test_translates_non_empty_fields(self):
        self.client.force_login(self.staff)
        with mock.patch("common.views.translate_fields", return_value={"title": {"uz": "Salom", "ru": "Привет"}}) as m:
            response = self.post({"fields": [
                {"key": "title", "text": "Hello", "max_length": 100},
                {"key": "empty", "text": "  "},
            ]})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"translations": {"title": {"uz": "Salom", "ru": "Привет"}}})
        m.assert_called_once_with([{"key": "title", "text": "Hello", "html": False, "max_length": 100}])

    def test_bad_payload(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.post({"nope": 1}).status_code, 400)

    def test_service_error_is_reported(self):
        self.client.force_login(self.staff)
        with mock.patch("common.views.translate_fields", side_effect=translation.TranslationError("not set up")):
            response = self.post({"fields": [{"key": "a", "text": "Hi"}]})
        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json()["error"], "not set up")


class TranslateFieldsTests(TestCase):
    def fake_response(self, payload, stop_reason="end_turn"):
        block = SimpleNamespace(type="text", text=json.dumps(payload))
        return SimpleNamespace(stop_reason=stop_reason, content=[block])

    @mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": ""})
    def test_missing_api_key(self):
        with self.assertRaises(translation.TranslationError):
            translation.translate_fields([{"key": "a", "text": "Hi"}])

    @mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    def test_parses_response_and_drops_unknown_keys(self):
        payload = {"translations": [
            {"key": "title", "uz": "Salom", "ru": "Привет"},
            {"key": "bogus", "uz": "x", "ru": "y"},
        ]}
        with mock.patch("common.translation.anthropic.Anthropic") as client_cls:
            create = client_cls.return_value.beta.messages.create
            create.return_value = self.fake_response(payload)
            result = translation.translate_fields([{"key": "title", "text": "Hello", "html": False}])
        self.assertEqual(result, {"title": {"uz": "Salom", "ru": "Привет"}})
        kwargs = create.call_args.kwargs
        self.assertEqual(kwargs["output_config"]["format"]["type"], "json_schema")
        self.assertIn("Hello", kwargs["messages"][0]["content"])

    @mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"})
    def test_refusal(self):
        with mock.patch("common.translation.anthropic.Anthropic") as client_cls:
            client_cls.return_value.beta.messages.create.return_value = self.fake_response({}, "refusal")
            with self.assertRaises(translation.TranslationError):
                translation.translate_fields([{"key": "a", "text": "Hi"}])
