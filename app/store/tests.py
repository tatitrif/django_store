from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback


class FeedbackTestCase(TestCase):
    feedback_url = reverse("store:feedback")

    valid_data = {
        "name": "fake_name",
        "email": "fake@email.com",
        "msg": "fake text",
        "captcha_0": "dummy",
        "captcha_1": "PASSED",
    }

    def test_feedback_form_valid(self):
        form = FeedbackForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_feedback_form_not_valid(self):
        # not email
        not_valid_data = {
            "name": "fake_name",
            "msg": "fake text",
            "captcha_0": "dummy",
            "captcha_1": "PASSED",
        }
        form = FeedbackForm(data=not_valid_data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, "email", "Это поле обязательно для заполнения.")

    def test_feedback_get(self):
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_feedback_post(self):
        self.client.post(self.feedback_url, self.valid_data, follow=True)
        self.assertTrue(Feedback.objects.filter(name=self.valid_data["name"]).exists())
