from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Profile


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]


class ProfileUpdateForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.FileInput)
    theme_image = forms.ImageField(required=False, widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ['image', 'theme_image', 'profession', 'about']
