# -*- coding: utf-8 -*-

'''
users/views
-----------

views for the users app
'''

import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    RedirectView,
    UpdateView,
)

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    Fieldset,
    Layout,
    Reset,
    Submit,
)

from .forms import UserInfoForm
from .models import Profile


logger = logging.getLogger('django')


class UserInfoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    '''
    user info update view
    '''

    form_class = UserInfoForm
    success_message = 'Successfully updated user info.'
    success_url = reverse_lazy('users:detail')
    template_name = 'users/user_update.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.helper = FormHelper()
        form.helper.layout = Layout(
            Fieldset(
                '',
                'first_name',
                'last_name',
                'country',
            ),
            FormActions(
                Submit('submit', 'Save'),
                Reset('reset', 'Cancel'),
            ),
        )

        return form

    def get_initial(self):
        initial = super().get_initial()
        profile = self.get_object()

        initial['first_name'] = profile.user.first_name
        initial['last_name'] = profile.user.last_name

        return initial

    def get_object(self):
        return self.request.user.profile


class UserRedirectView(LoginRequiredMixin, RedirectView):
    '''
    user redirect view
    '''

    permanent = False

    def get_redirect_url(self):
        return reverse('users:detail')
