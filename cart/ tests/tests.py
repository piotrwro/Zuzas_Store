from django.test import Client
import pytest


def client():
    client = Client()
    return client


@pytest.mark.django_db
def test_cart_add(client):
    client.login(username='piter', password='dorota2')

    response = client.get('/cart/views.cart.add')

    assert response.status_code == 200




