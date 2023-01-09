from django.db import models
from django.utils import timezone

from core.models import User

class Board(models.Model):
    class Meta:
        verbose_name = "Доска"
        verbose_name_plural = "Доски"

    title = models.CharField(verbose_name="Название", max_length=255)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего обновления')
    

class GoalCategory(models.Model):
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    board = models.ForeignKey(
        Board, verbose_name="Доска", on_delete=models.PROTECT, related_name="categories"
    )
    title = models.CharField(verbose_name="Название", max_length=255)
    user = models.ForeignKey(User, verbose_name="Автор", on_delete=models.PROTECT)
    is_deleted = models.BooleanField(verbose_name="Удалена", default=False)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Дата последнего обновления")


class Goal(models.Model):

    class Status(models.IntegerChoices):
        to_do = 1, "К выполнению"
        in_progress = 2, "В процессе"
        done = 3, "Выполнено"
        archived = 4, "Архив"

    class Priority(models.IntegerChoices):
        low = 1, "Низкий"
        medium = 2, "Средний"
        high = 3, "Высокий"
        critical = 4, "Критический"

    title = models.CharField(verbose_name='Назавание', max_length=255)
    description = models.TextField(verbose_name='Описание', null=True, blank=True)
    status = models.PositiveSmallIntegerField(
        verbose_name="Статус",
        choices=Status.choices,
        default=Status.to_do
    )
    priority = models.PositiveSmallIntegerField(
        verbose_name="Приоритет",
        choices=Priority.choices,
        default=Priority.medium
    )

    due_date = models.DateField(verbose_name='Дата выполнения', null=True, blank=True)
    user = models.ForeignKey(
        'core.User',
        verbose_name='Автор',
        on_delete=models.PROTECT
    )
    category = models.ForeignKey(
        GoalCategory,
        verbose_name='Категория',
        related_name='goals',
        on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now_add=True, verbose_name="Дата последнего обновления")
    

class GoalComment(models.Model):

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    text = models.TextField(verbose_name='Текст')
    goal = models.ForeignKey(
        Goal,
        verbose_name='Цель',
        on_delete=models.PROTECT,
        related_name='comments',
    )
    user = models.ForeignKey(
        'core.User',
        verbose_name='Пользователь',
        on_delete=models.PROTECT,
        related_name='comments',
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now_add=True, verbose_name='Дата последнего обновления')

class BoardParticipant(models.Model):
    class Meta:
        unique_together = ("board", "user")
        verbose_name = "Участник"
        verbose_name_plural = "Участники"

    class Role(models.IntegerChoices):
        owner = 1, "Владелец"
        writer = 2, "Редактор"
        reader = 3, "Читатель"

    board = models.ForeignKey(
        Board,
        verbose_name="Доска",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    user = models.ForeignKey(
        User,
        verbose_name="Пользователь",
        on_delete=models.PROTECT,
        related_name="participants",
    )
    role = models.PositiveSmallIntegerField(
        verbose_name="Роль", choices=Role.choices, default=Role.owner
    )
    created = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated = models.DateTimeField(auto_now=True, verbose_name="Дата последнего обновления")
