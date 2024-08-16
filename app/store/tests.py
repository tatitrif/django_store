from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback, PageInfo


class StoreModelViewTestCase(TestCase):
    def test_page_info(self):
        slug = "page_info_slug"
        page_info = PageInfo.objects.create(
            name="page_info_name",
            slug=slug,
        )
        count = PageInfo.objects.all().count()
        path = reverse("store:page_info", kwargs={"slug": page_info.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(count, 1)
        self.assertIn(page_info.slug, page_info.get_absolute_url())


class StoreUrlsTestCase(TestCase):
    def test_urls_home(self):
        response = self.client.get(reverse("store:home"))
        self.assertEqual(response.request["PATH_INFO"], reverse("store:home"))
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_feedback(self):
        response = self.client.get(reverse("store:feedback"))
        self.assertEqual(response.request["PATH_INFO"], reverse("store:feedback"))
        self.assertEqual(response.status_code, HTTPStatus.OK)


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
