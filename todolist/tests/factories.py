import factory.fuzzy
from django.contrib.auth import get_user_model

from goals.models import GoalCategory, Board, Goal, GoalComment, BoardParticipant

USER_MODEL = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = USER_MODEL

    username = factory.Faker('name')
    email = factory.Faker('email')
    password = 'PaSSword1022'


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('name')


class BoardParticipantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BoardParticipant

    board = factory.SubFactory(BoardFactory)
    user = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    board = factory.SubFactory(BoardFactory)
    title = factory.Faker('name')
    user = factory.SubFactory(UserFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker('name')
    user = factory.SubFactory(UserFactory)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalComment

    text = factory.fuzzy.FuzzyText(length=10)
    goal = factory.SubFactory(UserFactory)
    user = factory.SubFactory(GoalFactory)