import pytest
from django.conf import settings
from django.urls import reverse, resolve

pytestmark = pytest.mark.django_db


def test_detail(user: settings.AUTH_USER_MODEL):
    assert reverse("users:detail") == "/users/detail/"
    assert resolve("/users/detail/").view_name == "users:detail"
