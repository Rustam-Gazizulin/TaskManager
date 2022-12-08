
from rest_framework.generics import CreateAPIView
from rest_framework import permissions

from goals.models import GoalCategory


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    permission_classes = [permissions.IsAuthenticated]