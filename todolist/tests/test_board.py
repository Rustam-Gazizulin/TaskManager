import json

import pytest
from django.urls import reverse
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, BoardParticipant
from goals.serializers import BoardSerializer


@pytest.mark.django_db
def test_create(auth_user: APIClient, board: Board) -> None:
    response = auth_user.post(
        reverse('create-board'),
        data={
            'title': 'tests board',
        },
    )
    expected_response = {
        'id': response.data.get('id'),
        'title': 'tests board',
        'created': response.data.get('created'),
        'updated': response.data.get('updated'),
        'is_deleted': False,
    }

    assert response.status_code == 201
    assert response.data == expected_response




@pytest.mark.django_db
def test_retrieve(auth_user: APIClient, board: Board, add_user: User, board_participant: BoardParticipant) -> None:
    response = auth_user.get(reverse('Retrieve-Update-Destroy-board', args=[board.pk]))

    expected_response = BoardSerializer(instance=board).data

    assert response.status_code == 200
    assert response.data == expected_response


@pytest.mark.django_db
def test_delete(auth_user: APIClient, board: Board, add_user: User, board_participant: BoardParticipant) -> None:
    response = auth_user.delete(reverse('Retrieve-Update-Destroy-board', args=[board.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_user: APIClient, board: Board, add_user: User, board_participant: BoardParticipant) -> None:
    response = auth_user.put(
        reverse('Retrieve-Update-Destroy-board', args=[board.pk]),
        data=json.dumps({
            'title': 'put board',
            'participants': [],
        }),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('title') == 'put board'