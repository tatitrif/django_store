import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _


class Command(BaseCommand):
    help = "Creates an admin user non-interactively if it doesn't exist"

    def add_arguments(self, parser):
        parser.add_argument("--username", help=_("Admin username"))
        parser.add_argument("--email", help=_("Admin email"))
        parser.add_argument("--password", help=_("Admin password"))
        parser.add_argument(
            "--no-input",
            help=_("Read options from the environment"),
            action="store_true",
        )

    def handle(self, *args, **options):
        user = get_user_model()

        if options["no_input"]:
            options["username"] = os.environ["DJANGO_SUPERUSER_USERNAME"]
            options["email"] = os.environ["DJANGO_SUPERUSER_EMAIL"]
            options["password"] = os.environ["DJANGO_SUPERUSER_PASSWORD"]

        if not user.objects.filter(username=options["username"]).exists():
            user.objects.create_superuser(
                username=options["username"],
                email=options["email"],
                password=options["password"],
            )
