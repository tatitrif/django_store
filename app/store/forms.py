from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField(
        label=_("Enter text from image"),
    )

    name = forms.CharField(
        label=_("Your Name"),
        widget=forms.TextInput(attrs={"placeholder": _("Your Name")}),
    )
    email = forms.EmailField(
        label=_("E-Mail Address"),
        widget=forms.EmailInput(attrs={"placeholder": _("example@example.com")}),
    )
    msg = forms.CharField(
        label=_("Message"),
        widget=forms.Textarea(
            attrs={"cols": 60, "rows": 10, "placeholder": _("Message")}
        ),
    )

    class Meta:
        model = Feedback
        fields = [
            "name",
            "email",
            "msg",
        ]
