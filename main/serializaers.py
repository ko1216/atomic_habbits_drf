from rest_framework import serializers

from main.models import Habit
from main.validators import (DurationValidator,
                             validate_related_habits_with_reward,
                             validate_related_habits_type,
                             validate_pleasant_habit)


class HabitSerializer(serializers.ModelSerializer):
    duration = serializers.IntegerField(
        validators=[DurationValidator('duration')]
    )

    def validate(self, data):
        validate_related_habits_with_reward(data)
        validate_related_habits_type(data)
        validate_pleasant_habit(data)
        return data

    class Meta:
        model = Habit
        fields = '__all__'
