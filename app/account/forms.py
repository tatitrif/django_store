import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    PasswordChangeForm,
)
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Login"), widget=forms.TextInput(attrs={"placeholder": _("Login")})
    )
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ["username", "password"]


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        labels = {
            "username": _("Login"),
            "email": _("email"),
            "first_name": _("First Name"),
            "last_name": _("Last Name"),
            "password1": _("Password"),
            "password2": _("Confirm Password"),
        }
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": _("Login")}),
            "email": forms.EmailInput(attrs={"placeholder": _("example@example.com")}),
            "first_name": forms.TextInput(attrs={"placeholder": _("First Name")}),
            "last_name": forms.TextInput(attrs={"placeholder": _("Last Name")}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]
        if not email:
            raise forms.ValidationError(_("Can't be empty"))
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(_("This email already exists"))
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(
        disabled=True,
        label=_("Login"),
        widget=forms.TextInput(attrs={"placeholder": _("Login")}),
    )
    email = forms.EmailField(
        disabled=True,
        required=False,
        label=_("E-mail"),
        widget=forms.TextInput(attrs={"placeholder": _("example@example.com")}),
    )

    class Meta:
        model = get_user_model()
        fields = ["image", "username", "email", "date_birth", "first_name", "last_name"]
        labels = {
            "first_name": _("First name"),
            "last_name": _("Last name"),
        }
        years_to_display = range(
            datetime.datetime.now().year - 10, datetime.datetime.now().year + 110
        )
        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": _("First Name")}),
            "last_name": forms.TextInput(attrs={"placeholder": _("Last Name")}),
            "date_birth": forms.SelectDateWidget(attrs={"years": years_to_display}),
            "image": forms.FileInput(),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label=_("Old Password"), widget=forms.PasswordInput()
    )
    new_password1 = forms.CharField(
        label=_("New Password"), widget=forms.PasswordInput()
    )
    new_password2 = forms.CharField(
        label=_("Confirm Password"), widget=forms.PasswordInput()
    )
