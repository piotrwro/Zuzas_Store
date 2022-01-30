import uuid
import pytest
from django.contrib.auth.models import User

from zuzas_store.models import Category


@pytest.fixture(scope='function')
def user():
    return User.objects.create_user('bob', 'bob@test.com', 'TestPass123')


@pytest.fixture(scope='function')
def test_password():
    return'TestPass123'


@pytest.fixture(scope='function')
def create_user(db, django_user_model, test_password):
    def make_user(**kwargs):
        kwargs['password'] = test_password

        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())

        return django_user_model.objects.create_user(**kwargs)

    return make_user

@pytest.fixture(scope='function')
def category():
    return Category.objects.create(name='Garaż')