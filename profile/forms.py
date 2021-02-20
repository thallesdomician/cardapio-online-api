from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import password_validation
from django.contrib.auth.forms import (
    AuthenticationForm
)

from profile.models import Profile


class CreateForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autofocus': True, 'autocomplete': 'email', 'class': 'form-control',
                   'placeholder': _('Email address')})
    )
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': _('Password')}),
        help_text=password_validation.password_validators_help_texts(),
    )

    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'password', 'class': 'form-control', 'placeholder': _('Password confirmation')}),
        strip=False,
        help_text=[_("Enter the same password as before, for verification.")],

    )

    username = UsernameField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}))

    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    # email = forms.EmailField(
    #     label=_("Email"),
    #     max_length=254,
    #     required=False,
    #     widget=forms.EmailInput(
    #         attrs={'readonly': 'readonly', 'class': 'form-control',
    #                'placeholder': _('Email address')})
    # )
    #
    # username = UsernameField(required=False,
    #                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Username')}))
    birth_date = forms.DateField(required=False, widget=forms.DateInput(format='%Y-%m-%d',
                                                                        attrs={'class': 'form-control',
                                                                               'type': 'date',
                                                                               'placeholder': _('Birth Date')}))
    #
    image = forms.ImageField(required=True,
                             widget=forms.FileInput(attrs={'class': 'form-control-file', 'placeholder': _('Image')}))
    phone = forms.CharField(required=False,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Phone')}))
    # first_name = forms.CharField(required=False,
    #                              widget=forms.TextInput(
    #                                  attrs={'class': 'form-control', 'placeholder': _('First Name')}))
    # last_name = forms.CharField(required=False,
    #                             widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Last Name')}))

    class Meta:
        model = Profile
        fields = ['image', 'birth_date', 'phone',]

    def save(self, user=None):
        user_profile = super(ProfileUpdateForm, self).save(commit=False)
        if user:
            user_profile.user = user
        user_profile.save()
        return user_profile


class AuthenticationProfileForm(AuthenticationForm):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(
        widget=forms.TextInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': _('Username')}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': _('Password')}),
    )
