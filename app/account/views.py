from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, UpdateView

from .forms import (
    LoginUserForm,
    RegisterUserForm,
    ProfileUserForm,
    UserPasswordChangeForm,
)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = "account/login.html"
    redirect_authenticated_user = True
    extra_context = {
        "button_text": _("Continue"),
    }


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "account/register.html"
    success_url = reverse_lazy("account:login")
    extra_context = {
        "button_text": _("Submit"),
    }


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = "account/profile.html"

    extra_context = {
        "button_text": _("Update"),
    }

    def get_success_url(self):
        return reverse_lazy("account:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy("account:password_change_done")
    template_name = "account/password_change_form.html"
