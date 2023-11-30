from rest_framework import status, serializers
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from main.models import Habit
from main.pagination import HabitPagination
from main.permissions import IsOwner
from main.serializaers import HabitSerializer


class PublicHabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)

    def get(self, request, *args, **kwargs):
        ordering = self.request.query_params.get('ordering', 'id')
        queryset = self.get_queryset().order_by(ordering)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class HabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Habit.objects.filter(owner=self.request.user).distinct()

    def get(self, request, *args, **kwargs):
        ordering = self.request.query_params.get('ordering', 'id')
        queryset = self.get_queryset().order_by(ordering)
        paginated_queryset = self.paginate_queryset(queryset)
        serializer = HabitSerializer(paginated_queryset, many=True)
        return self.get_paginated_response(serializer.data)


class HabitRetrieveAPIView(RetrieveAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data.copy()

        related_habits_ids = data.pop('related_habits', [])
        if len(related_habits_ids) > 1:
            raise serializers.ValidationError({'error': 'You can only provide one related habit.'})

        serializer.validated_data['related_habits'] = related_habits_ids
        habit = serializer.save()
        habit.create_reminder_task()

        if related_habits_ids:
            related_habit = Habit.objects.get(id=related_habits_ids[0])
            habit.related_habits.add(related_habit)
            related_habit.related_habits.add(habit)

        return habit


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]


class HabitDestroyAPIView(DestroyAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
