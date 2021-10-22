from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import CheckboxInput
# from django.contrib.auth.models import User
from .models import CustomUser
from captcha.fields import CaptchaField


class UserCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True, label="Nome")
    last_name = forms.CharField(required=True, label="Sobrenome")
    email = forms.EmailField(required=True, label='Email')
    captcha = CaptchaField()

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email",
                  "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
