from django.forms import EmailField
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    email = EmailField(
        label=_("Email address"),
        required=True,
        help_text=_("Required."))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        unique_together = ('email',)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        self.clean_email()
        if commit:
            user.save()
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return email
