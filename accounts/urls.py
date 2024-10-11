from django.contrib.auth.views import PasswordResetView
from django.urls import include, path
from django.views.generic import TemplateView

from .views import EmailVerify, MyLoginView, RegisterView

urlpatterns = [
    path("login/", MyLoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "password_reset/",
        PasswordResetView.as_view(
            template_name="registration/my_password_reset_form.html"
        ),
        name="password_reset",
    ),
    path("", include("django.contrib.auth.urls")),
    path(
        "verify_email/<uidb64>/<token>/",
        EmailVerify.as_view(),
        name="verify_email",
    ),
    path(
        "confirm_email/",
        TemplateView.as_view(template_name="registration/confirm_email.html"),
        name="confirm_email",
    ),
    path(
        "invalid_verify/",
        TemplateView.as_view(template_name="registration/invalid_verify.html"),
        name="invalid_verify",
    ),
]
