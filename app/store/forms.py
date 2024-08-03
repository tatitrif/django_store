from captcha.fields import CaptchaField
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    captcha = CaptchaField(label=_("Captcha label"))

    class Meta:
        model = Feedback
        fields = [
            "name",
            "email",
            "msg",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-input"}),
            "msg": forms.Textarea(attrs={"cols": 50, "rows": 5}),
        }

    name = forms.CharField(label=_("Name"))
    email = forms.EmailField(label=_("Email"))
    msg = forms.CharField(
        label=_("Message"), widget=forms.Textarea(attrs={"cols": 60, "rows": 10})
    )
