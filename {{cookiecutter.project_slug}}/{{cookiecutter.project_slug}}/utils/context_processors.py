# -*- coding: utf-8 -*-

'''
utils/context_processors
--------------------------

project context processors
'''

from django.conf import settings

from {{ cookiecutter.project_slug }} import __version__


def globals_context(request):
    '''
    injects selected variables into templates
    '''

    return {
        'app_version': __version__,
    }


def settings_context(request):
    '''
    injects settings into templates
    '''

    return {
        'settings': settings,
    }
