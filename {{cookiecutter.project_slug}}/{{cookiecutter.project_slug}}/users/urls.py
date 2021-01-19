# -*- coding: utf-8 -*-

'''
users/urls
----------

urls for the users app
'''

from django.urls import path

from .views import UserInfoUpdateView


app_name = 'users'

urlpatterns = [

    path(
        'detail/',
        UserInfoUpdateView.as_view(),
        name='detail',
    ),
]
