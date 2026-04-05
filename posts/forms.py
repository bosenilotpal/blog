from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordResetForm,
    UserCreationForm,
)
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
# Create your forms here.
class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-control'}))
    password = forms.CharField(max_length=50,
                               required=True,
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'password')


class PasswordResetFormPrintToken(PasswordResetForm):
    """Does not send email; prints reset uid/token to the server process stdout."""

    def save(self, domain_override=None, **kwargs):
        request = kwargs.get("request")
        token_generator = kwargs.get("token_generator", default_token_generator)
        email = self.cleaned_data["email"]
        for user in self.get_users(email):
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            lines = [
                "",
                "=" * 60,
                "[PASSWORD RESET] (no email; use this in the server terminal)",
                f"  email: {email}",
                f"  username: {user.get_username()}",
                f"  uidb64: {uid}",
                f"  token: {token}",
            ]
            if request is not None:
                from django.urls import reverse

                rel = reverse(
                    "password_reset_confirm",
                    kwargs={"uidb64": uid, "token": token},
                )
                lines.append(f"  reset path: {rel}")
            lines.append("=" * 60)
            print("\n".join(lines), flush=True)
        return None