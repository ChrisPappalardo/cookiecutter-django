from copy import copy
import pytest

from django.conf import settings
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory

from {{ cookiecutter.project_slug }}.users.forms import (
    ResetPasswordForm,
    UserInfoForm,
    UserSignupForm,
)
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestResetPasswordForm:
    user = UserFactory.build()
    form_data = {"email": user.email, "g-recaptcha-response": "foo"}

    def test_form_is_valid(self):
        form = ResetPasswordForm(self.form_data)
        assert form.is_valid()


class TestUserInfoForm:
    user = UserFactory.build()
    form_data = {
        "first_name": user.last_name,
        "last_name": user.first_name,
        "country": "US",
    }

    def test_form_is_valid(self):
        form = UserInfoForm(self.form_data)
        assert form.is_valid()

    def test_form_is_invalid(self):
        form_data = copy(self.form_data)
        form_data["country"] = False
        form = UserInfoForm(form_data)
        assert not form.is_valid()


class TestUserSignupForm:
    user = UserFactory.build()
    form_data = {
        "username": user.username,
        "email": user.email,
        "password1": "#MyPassword123!",
        "password2": "#MyPassword123!",
        "g-recaptcha-response": "foo",
    }

    def test_form_is_valid(self):
        form = UserSignupForm(self.form_data)
        assert form.is_valid()

    def test_form_is_invalid(self):
        form_data = copy(self.form_data)
        form_data["email"] = "foo"
        form = UserSignupForm(form_data)
        assert not form.is_valid()

    def test_username_is_email(self):
        if settings.ACCOUNT_AUTHENTICATION_METHOD == "email":
            request = RequestFactory().get("/")
            middleware = SessionMiddleware()
            middleware.process_request(request)
            request.session.save()
            form = UserSignupForm(self.form_data)
            form.is_valid()
            form.save(request)
            assert form.cleaned_data["username"] == form.cleaned_data["email"]
