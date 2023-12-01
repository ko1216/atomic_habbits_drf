from rest_framework import serializers

from main.models import HabitType, Habit


class DurationValidator:

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if int(value) > 120:
            raise serializers.ValidationError(
                'Duration must be more than 120 seconds'
            )
        if int(value) < 1:
            raise serializers.ValidationError(
                'Duration cannot be less than 1 second'
            )


def validate_related_habits_with_reward(value):
    related_habits = value.get('related_habits')
    reward = value.get('reward')

    if related_habits and reward:
        raise serializers.ValidationError(
            {
                'detail': 'Cannot choose both related habits and a reward'
            }
        )


def validate_related_habits_type(value):
    related_habits = value.get('related_habits', [])

    if related_habits:
        related_habit = related_habits[0].id

        try:
            related_habit = Habit.objects.get(pk=related_habit)
        except Habit.DoesNotExist:
            raise serializers.ValidationError(
                'Related habit not found'
            )

        if related_habit.habit_type == HabitType.useful:
            raise serializers.ValidationError(
                {
                    'detail': 'Related habits cannot be of type "useful"'
                }
            )


def validate_pleasant_habit(value):
    habit_type = value.get('habit_type')
    reward = value.get('reward')
    related_habits = value.get('related_habits')

    if habit_type == HabitType.pleasant and (reward or related_habits):
        raise serializers.ValidationError(
            {
                'detail':
                    'Pleasant habbit cannot have reward or related_habbits'
            }
        )
