from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm as DjangoAuthenticationForm
from django.contrib.auth.forms import UserChangeForm as DjangoUserChangeForm
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from accounts.utils import send_email_for_verify

User = get_user_model()


class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        label=_("email address"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )
    phone = forms.CharField(
        label=_("Телефон"),
    )

    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        cleaned_data["phone"] = (
            phone.replace(" ", "").replace("(", "").replace(")", "").replace("-", "")
        )
        return cleaned_data

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "phone")


class AuthenticationForm(DjangoAuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username is not None and password:
            self.user_cache = authenticate(
                self.request,
                username=username,
                password=password,
            )
            if self.user_cache is None:
                raise self.get_invalid_login_error()
            elif not self.user_cache.is_verified:
                send_email_for_verify(self.request, self.user_cache)
                raise ValidationError(
                    "Email not verify, check your email",
                    code="invalid_login",
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class UserChangeForm(DjangoUserChangeForm):
    class Meta:
        model = User
        fields = ("username", "email", "phone", "groups")
