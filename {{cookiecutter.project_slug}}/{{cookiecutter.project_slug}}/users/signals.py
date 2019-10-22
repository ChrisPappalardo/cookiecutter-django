# -*- coding: utf-8 -*-

'''
users/signals
-------------

signals for the users app
'''

import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_login_failed
from django.dispatch import receiver

from allauth.account.signals import (
    user_logged_in,
    user_logged_out,
    user_signed_up,
)
from djcorecap.utils import get_client_ip


logger = logging.getLogger('django')


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    '''
    handle user_logged_in signals
    '''

    v = (user.username, user.id, get_client_ip(request))
    logger.warning('%s (ID %s) logged in from %s' % (v))


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):
    '''
    handle user_logged_out signals
    '''

    v = (user.username, user.id, get_client_ip(request))
    logger.warning('%s (ID %s) logged out from %s' % (v))


@receiver(user_signed_up)
def user_signed_up_callback(sender, request, user, **kwargs):
    '''
    handle user_signed_up signals
    '''

    v = (user.username, user.id, get_client_ip(request))
    logger.warning('%s (ID %s) signed up from %s' % (v))


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, request, **kwargs):
    '''
    handle user_login_failed signals
    '''

    u = credentials.get('username', None)
    exists = True if get_user_model().objects.filter(username=u) else False

    v = (u, exists, get_client_ip(request))
    logger.warning('failed login attempt for %s (exists %s) from %s' % (v))
