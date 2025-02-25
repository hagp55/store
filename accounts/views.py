from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode
from django.views import View

from .forms import AuthenticationForm, UserCreationForm
from .utils import send_email_for_verify

User = get_user_model()


class MyLoginView(LoginView):
    form_class = AuthenticationForm


class EmailVerify(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)

        if user is not None and token_generator.check_token(user, token):
            user.is_verified = True
            user.save()
            login(request, user)
            return redirect("index")
        return redirect("invalid_verify")

    @staticmethod
    def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            User.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user


class RegisterView(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {"form": UserCreationForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")

            user = authenticate(email=email, password=password)
            send_email_for_verify(request, user)
            return redirect("confirm_email")
        else:
            context = {"form": form}
            return render(request, self.template_name, context)
