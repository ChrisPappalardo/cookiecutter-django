# -*- coding: utf-8 -*-

'''
users/urls
----------

urls for the users app
'''

from django.urls import path

from .views import (
    UserInfoUpdateView,
    UserRedirectView,
)


app_name = 'users'

urlpatterns = [

    path(
        'detail/',
        UserInfoUpdateView.as_view(),
        name='detail',
    ),

    path(
        'redirect/',
        UserRedirectView.as_view(),
        name='redirect',
    ),
]
