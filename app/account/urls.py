from django.contrib.auth.views import (
    LogoutView,
    PasswordChangeDoneView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.urls import path
from django.urls import reverse_lazy

from .views import (
    LoginUser,
    RegisterUser,
    UserPasswordChange,
    ProfileUser,
)

app_name = "account"

urlpatterns = [
    path(
        "register/",
        RegisterUser.as_view(),
        name="register",
    ),
    path(
        "",
        ProfileUser.as_view(),
        name="profile",
    ),
    path(
        "login/",
        LoginUser.as_view(next_page="account:profile"),
        name="login",
    ),
    path("logout/", LogoutView.as_view(next_page="account:login"), name="logout"),
    path(
        "password-change/",
        UserPasswordChange.as_view(),
        name="password_change",
    ),
    path(
        "password-change/done/",
        PasswordChangeDoneView.as_view(
            template_name="account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        PasswordResetView.as_view(
            template_name="account/password_reset_form.html",
            email_template_name="account/password_reset_email.html",
            success_url=reverse_lazy("account:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(
            template_name="account/password_reset_confirm.html",
            success_url=reverse_lazy("account:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(
            template_name="account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]