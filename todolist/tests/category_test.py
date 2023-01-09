import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, GoalCategory
from goals.serializers import GoalCategorySerializer


@pytest.mark.django_db
def test_create(auth_user: APIClient, add_user: User, board: Board, board_participant) -> None:
    response = auth_user.post(
        reverse('create_category'),
        data={
           'title': 'tests category',
           'user': add_user.pk,
           'board': board.pk,
        },
    )
    expected_response = {
        'id': response.data.get('id'),
        'title': 'tests category',
        'board': board.pk,
        'created': response.data.get('created'),
        'updated': response.data.get('updated'),
        'is_deleted': False,
    }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_user: APIClient, add_user: User, category: GoalCategory, board: Board) -> None:
    response = auth_user.get(reverse('Retrieve-Update-Destroy-category', args=[category.pk]))

    expected_response = GoalCategorySerializer(instance=category).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_user: APIClient, board: Board, category: GoalCategory) -> None:
    response = auth_user.delete(reverse('Retrieve-Update-Destroy-category', args=[category.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_user: APIClient, board: Board, add_user: User, category: GoalCategory) -> None:
    response = auth_user.put(
        reverse('Retrieve-Update-Destroy-category', args=[category.pk]),
        data=json.dumps({
            'title': 'put category',
            'board': board.pk
        }),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('title') == 'put category'