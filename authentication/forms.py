from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from django.core import validators
from django.core.exceptions import ValidationError


def get_error(key, value=""):
    error_messages = {
        "password_mismatch": "The two password fields didn't match to each other.",
        "user_exists": f"A user with that username {value} already exists.",
        "numeric_password": "Your password can't be entirely numeric.",
        "short_password": "Your password must contain at least 8 characters.",
        "email_exists": f"A user with that email {value} already exists."
    }
    return error_messages[key]


class RegisterForm(UserCreationForm):
    username = forms.CharField(min_length=5, max_length=50,
                               validators=[validators.MaxLengthValidator, validators.MinLengthValidator])
    email = forms.EmailField()
    first_name = forms.CharField(max_length=50, validators=[validators.MaxLengthValidator])
    last_name = forms.CharField(max_length=100, validators=[validators.MaxLengthValidator])
    password1 = forms.PasswordInput()
    password2 = forms.PasswordInput()

    class Meta:
        model = get_user_model()
        # model = User
        fields = ["username", "email", "first_name", "last_name", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data['username']
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError(get_error("user_exists", value=username))
            # raise forms.ValidationError(f"A user with that username {username} already exists.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError(get_error("password_mismatch"))
            # raise forms.ValidationError("The two password fields didn't match to each other.")
        if password1.isnumeric():
            raise ValidationError(get_error("numeric_password"))
            # raise forms.ValidationError("Your password can't be entirely numeric.")
        if len(password1) < 8:
            raise ValidationError(get_error("short_password"))
            # raise forms.ValidationError("Your password must contain at least 8 characters.")
        return password2

    def clean_email(self):
        email = self.cleaned_data["email"]
        if get_user_model().objects.filter(email__iexact=email).exists():
            raise ValidationError(get_error("email_exists", value=email))
            # raise forms.ValidationError(f"A user with that email '{email}' already exists.")
        return email


class EditRegisterForm(forms.ModelForm):
    # password = None
    class Meta:
        model = get_user_model()
        # model = User
        fields = ['username', 'email', 'first_name', 'last_name', ]


class NewPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox(), label='')


class CustomSetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']
