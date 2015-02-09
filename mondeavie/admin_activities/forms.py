# -*- coding: utf-8 -*-

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,\
                                PasswordResetForm, SetPasswordForm

from django.utils.translation import ugettext, ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Field, Button

from localflavor import ca

class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, label = '', 
                widget=forms.TextInput(attrs={'placeholder': 'Usage'}))
    password = forms.CharField(required=True, label='', 
            widget=forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}))

    next = forms.CharField()

    def __init__(self, *args, **kwargs):
        next = kwargs.pop('next', '/')
        super(LoginForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('next', value=next, type="hidden"),
            Field('username', id="username"),
            Field('password', id="password", title="Mot de passe"),
            ButtonHolder(
                Submit('login', 'Connection', css_class='btn-primary')
            )
        )