import pytest
from django.conf import settings
from django.test import RequestFactory

from {{ cookiecutter.project_slug }}.users.views import UserInfoUpdateView

pytestmark = pytest.mark.django_db


class TestUserUpdateView:
    def test_get_object(
        self, user: settings.AUTH_USER_MODEL, request_factory: RequestFactory
    ):
        view = UserInfoUpdateView()
        request = request_factory.get("/fake-url/")
        request.user = user

        view.request = request

        assert view.get_object().user == user
