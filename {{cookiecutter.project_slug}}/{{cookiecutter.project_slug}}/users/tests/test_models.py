import pytest
from django.conf import settings
from django.contrib.auth import get_user_model

pytestmark = pytest.mark.django_db


def test_user_class(user: settings.AUTH_USER_MODEL):
    assert isinstance(user, get_user_model())
