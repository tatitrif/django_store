from django.conf import settings
from django.test import TestCase


class ChatSettingsTestCase(TestCase):
    def test_installed_apps(self):
        self.assertIn("daphne", settings.INSTALLED_APPS)
        self.assertIn("chat.apps.ChatConfig", settings.INSTALLED_APPS)

    def test_asgi_application(self):
        self.assertEqual(settings.ASGI_APPLICATION, "config.asgi.application")

    def test_channel_layers(self):
        self.assertEqual(
            "channels.layers.InMemoryChannelLayer",
            settings.CHANNEL_LAYERS["default"]["BACKEND"],
        )
