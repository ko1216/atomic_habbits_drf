from rest_framework.permissions import BasePermission

from main.models import Habit


class IsOwner(BasePermission):

    message = 'Вы не являетесь владельцем этой записи'

    def has_object_permission(self, request, view, obj):
        return Habit.objects.filter(owner=request.user, pk=obj.pk).exists()
