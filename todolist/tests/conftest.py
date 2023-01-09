import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from core.models import User
from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment
from tests.factories import (
    BoardFactory,
    BoardParticipantFactory,
    CategoryFactory,
    GoalFactory,
    CommentFactory,
)

USER_MODEL = get_user_model()


@pytest.fixture
def auth_user(add_user: User) -> APIClient:
    client = APIClient()
    client.login(username='john', password='test1234')
    return client


@pytest.fixture
def add_user(db) -> User:
    user = USER_MODEL.objects.create_user(
        username='john',
        email='john@gmail.com',
        password='test1234'
    )
    return user


@pytest.fixture
def board() -> Board:
    return BoardFactory.create()


@pytest.fixture
def board_participant(add_user: User, board: Board) -> BoardParticipant:
    return BoardParticipantFactory.create(user=add_user, board=board)


@pytest.fixture
def category(board: Board, add_user: User, board_participant: BoardParticipant) -> GoalCategory:
    return CategoryFactory.create(board=board, user=add_user)


@pytest.fixture
def goal(category: GoalCategory, add_user: User) -> Goal:
    return GoalFactory.create(user=add_user, category=category)


@pytest.fixture
def comment(goal: Goal, add_user: User) -> GoalComment:
    return CommentFactory.create(user=add_user, goal=goal)
