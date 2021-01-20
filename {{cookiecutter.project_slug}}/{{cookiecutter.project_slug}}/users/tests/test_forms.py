from copy import copy
import pytest

from {{ cookiecutter.project_slug }}.users.forms import UserSignupForm
from {{ cookiecutter.project_slug }}.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


# TODO: custom add reset password and user info form tests


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

    # TODO: add custom save test
