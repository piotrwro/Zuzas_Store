
import pytest
from django.contrib.auth.models import User
from zuzas_store.models import Category


@pytest.mark.django_db
def test_category(category):
    count = Category.objects.all().count()
    assert count == 1

@pytest.mark.django_db
def test_user_create(user):
    count = User.objects.all().count()
    assert count == 1


@pytest.mark.django_db
def test_check_password(user):
    user.set_password('secret')
    assert user.check_password('secret') is True




