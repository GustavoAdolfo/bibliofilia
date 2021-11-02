from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    PasswordChangeForm
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


class UserChangeForm(UserChangeForm):
    email = forms.EmailField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    first_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        # fields = ['username', 'first_name', 'last_name', 'email']
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        # self.fields['username'].widget.attrs['class'] = 'form-control'
        # self.fields['username'].help_text = '<div class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></div>'
        self.fields['password'].help_text = "Click <a href=\"../changepassword/\"> Here</a to reset your Password."


class PasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
