import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from core.serializers import ProfileSerializer


@pytest.mark.django_db
def test_create(client: APIClient) -> None:
    data = {
        'username': 'djohn',
        'email': 'djohn@gmail.com',
        'password': 'SuperPassword1022',
        'password_repeat': 'SuperPassword1022',
    }
    response = client.post(
        reverse('signup'),
        data=data,
    )
    user = User.objects.order_by('-pk').first()
    expected_response = {
        'id': response.data.get('id'),
        'first_name': '',
        'last_name': '',
        'username': 'djohn',
        'email': 'djohn@gmail.com',
    }

    assert response.status_code == 201
    assert response.data == expected_response
    assert user.is_superuser is False


@pytest.mark.django_db
def test_profile(auth_user: APIClient, add_user: User) -> None:
    response = auth_user.get(reverse('profile'))
    expected_response = ProfileSerializer(instance=add_user).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_update_password(auth_user: APIClient, add_user: User) -> None:
    response = auth_user.put(
        reverse('update_password'),
        data={
            'new_password': 'SuperPassword1022362',
            'old_password': 'test1234',
        },
    )

    assert response.status_code == 200