from rest_framework import permissions

from goals.models import BoardParticipant


class BoardPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class GoalCategoryPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, category):
        if not request.user.is_authenticated:
            return False
        if permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ]
        ).exists()