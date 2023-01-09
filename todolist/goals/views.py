from typing import List

from django.db import transaction
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions, filters, generics
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalCategory, Goal, Board
from goals.filters import GoalDateFilter

from goals.models import GoalComment
from goals.permissions import BoardPermissions, GoalCategoryPermissions, GoalPermissions, CommentsPermissions
from goals.serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, \
    GoalSerializer, GoalCommentCreateSerializer, GoalCommentSerializer, BoardCreateSerializer, BoardSerializer


class GoalCategoryCreateView(CreateAPIView):
    """ Создаем категорию для целей"""
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = GoalCategoryCreateSerializer


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [GoalCategoryPermissions]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ["board"]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self) -> List[GoalCategory]:
        return GoalCategory.objects.prefetch_related("board__participants").filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    """
    Создание категории для цели
    """
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [GoalCategoryPermissions]

    def get_queryset(self):
        return GoalCategory.objects.prefetch_related("board__participants").filter(
            board__participants__user_id=self.request.user.id, is_deleted=False
        )

    def perform_destroy(self, instance):
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=("is_deleted",))
            Goal.objects.filter(category=instance).update(status=Goal.Status.archived)
        return instance


class GoalCreateView(generics.CreateAPIView):
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalListView(generics.ListAPIView):
    model = Goal
    permission_classes = [GoalPermissions]
    serializer_class = GoalSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = GoalDateFilter
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return Goal.objects.select_related("user", "category__board").filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )


class GoalView(generics.RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [GoalPermissions]

    def get_queryset(self):
        return Goal.objects.select_related("user", "category__board").filter(
            Q(category__board__participants__user_id=self.request.user.id) & ~Q(status=Goal.Status.archived)
        )

    def perform_destroy(self, instance: Goal):
        """
        При удалении цели у нее меняется поле статус на "В архиве"
        """
        instance.status = Goal.Status.archived
        instance.save(update_fields=("status",))
        return instance


class GoalCommentCreateView(generics.CreateAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentCreateSerializer


class GoalCommentListView(generics.ListAPIView):
    model = GoalComment
    permission_classes = [CommentsPermissions]
    serializer_class = GoalCommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["goal"]
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.select_related("goal__category__board", "user").filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class GoalCommentView(generics.RetrieveUpdateDestroyAPIView):
    model = GoalComment
    serializer_class = GoalCommentSerializer
    permission_classes = [CommentsPermissions]

    def get_queryset(self):
        return GoalComment.objects.select_related("goal__category__board", "user").filter(
            goal__category__board__participants__user_id=self.request.user.id
        )


class BoardCreateView(generics.CreateAPIView):
    serializer_class = BoardCreateSerializer
    permission_classes = [BoardPermissions]


class BoardListView(generics.ListAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination
    ordering = ["title"]

    def get_queryset(self):
        return Board.objects.filter(participants__user_id=self.request.user.id, is_deleted=False)


class BoardView(generics.RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [BoardPermissions]
    serializer_class = BoardSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Board.objects.prefetch_related("participants").filter(
            participants__user_id=self.request.user.id, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» в архив категории, обновляем статус связанных целей на архивные
        with transaction.atomic():
            instance.is_deleted = True
            instance.save(update_fields=("is_deleted",))
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance