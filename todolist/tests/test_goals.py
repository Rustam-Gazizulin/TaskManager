import json
from datetime import datetime
from rest_framework.test import APIClient
import pytest
from django.urls import reverse

from core.models import User
from goals.models import GoalCategory, Goal
from goals.serializers import GoalSerializer


@pytest.mark.django_db
def test_create(auth_user: APIClient, add_user: User, category: GoalCategory) -> None:
    test_date = str(datetime.now().date())
    response = auth_user.post(
        reverse("create_goal"),
        data={
            "title": "tests goal",
            "user": add_user.pk,
            "category": category.pk,
            "description": 'This is nice goal',
            "due_date": test_date,
        },
    )
    expected_response = {
        "id": response.data.get("id"),
        "title": "tests goal",
        "description": response.data.get("description"),
        "due_date": response.data.get("due_date"),
        "status": 1,
        "priority": 2,
        "category": category.pk,
        "created": response.data.get("created"),
        "updated": response.data.get("updated"),
    }

    assert response.status_code == 201
    assert response.data == expected_response


@pytest.mark.django_db
def test_retrieve(auth_user: APIClient, goal: Goal, add_user: User, category: GoalCategory) -> None:
    response = auth_user.get(reverse('Retrieve-Update-Destroy-goal', args=[goal.pk]))

    expected_response = GoalSerializer(instance=goal).data

    assert response.status_code == 200
    assert response.data == expected_response



@pytest.mark.django_db
def test_delete(auth_user: APIClient, goal: Goal, category: GoalCategory) -> None:
    response = auth_user.delete(reverse('Retrieve-Update-Destroy-goal', args=[goal.pk]))

    assert response.status_code == 204


@pytest.mark.django_db
def test_update(auth_user: APIClient, goal: Goal, add_user: User, category: GoalCategory) -> None:
    response = auth_user.put(
        reverse('Retrieve-Update-Destroy-goal', args=[goal.pk]),
        data=json.dumps({
            'title': 'put goal',
            'category': category.pk
        }),
        content_type='application/json'
    )

    assert response.status_code == 200
    assert response.data.get('title') == 'put goal'
