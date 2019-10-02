# -*- coding: utf-8 -*-

'''
users/admin
-----------

admin settings for the users app
'''

from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model

from .models import Profile


User = get_user_model()


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    fieldsets = (
        ('misc', {'fields': (
            'country',
        )}),
    )
    verbose_name_plural = 'Profile'


class UserAdmin(auth_admin.UserAdmin):
    inlines = auth_admin.UserAdmin.inlines + [ProfileInline]
    list_display = [
        'username',
        'first_name',
        'last_name',
        'email',
        'get_country',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
    ]
    search_fields = [
        'first_name',
        'last_name',
    ]

    def get_country(self, instance):
        return instance.profile.country
    get_country.short_description = 'Country'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
if settings.DEBUG:
    admin.site.register(Profile)
