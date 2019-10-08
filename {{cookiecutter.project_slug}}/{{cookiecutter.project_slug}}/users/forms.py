# -*- coding: utf-8 -*-

'''
users/forms
-----------

forms for the users app
'''

import logging

from django.forms import ModelForm, CharField

from allauth.account.adapter import get_adapter
from allauth.account.forms import ResetPasswordForm as _ResetPasswordForm
from allauth.account.utils import filter_users_by_email
from captcha.fields import ReCaptchaField

from .models import Profile


logger = logging.getLogger('django')


class ResetPasswordForm(_ResetPasswordForm):
    '''
    custom password reset form
    '''

    captcha = ReCaptchaField(label='')

    def clean_email(self):
        '''
        suppress non-existing email validation error
        '''

        email = self.cleaned_data['email']
        email = get_adapter().clean_email(email)
        self.users = filter_users_by_email(email)

        if not self.users:
            logger.error(f'non-existent email reset attempt on {email}')

        return self.cleaned_data['email']


class UserInfoForm(ModelForm):
    '''
    user info form
    '''

    first_name = CharField(max_length=30)
    last_name = CharField(max_length=150)

    class Meta:
        model = Profile
        fields = (
            'country',
        )

    def save(self, *args, **kwargs):
        self.update_name(self.instance.user)
        return super().save(*args, **kwargs)

    def update_name(self, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()


class UserSignupForm(UserInfoForm):
    '''
    user signup form with recaptcha
    '''

    captcha = ReCaptchaField(label='')

    field_order = [
        'username',
        'email',
        'password1',
        'password2',
        'first_name',
        'last_name',
        'country',
        'captcha',
    ]

    def signup(self, request, user):
        self.update_name(user)
        user.profile.country = self.cleaned_data['country']
        user.profile.save()
