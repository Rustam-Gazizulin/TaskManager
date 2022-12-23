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
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ]
        ).exists()


class GoalPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, goal):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(user=request.user, board=goal.category.board).exists()
        return BoardParticipant.objects.filter(
            user=request.user,
            board=goal.category.board,
            role__in=[
                BoardParticipant.Role.owner,
                BoardParticipant.Role.writer,
            ]
        ).exists()
    
class CommentPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, comment):
        if not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return BoardParticipant.objects.filter(
                user=request.user,
                board=comment.goal.category.board,
                role__in=[
                    BoardParticipant.Role.owner,
                    BoardParticipant.Role.writer,
                ]
            ).exists()
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return comment.user == request.user

