from rest_framework import serializers

from main.models import Habit
from main.validators import DurationValidator


class HabitSerializer(serializers.ModelSerializer):
    related_habits = serializers.PrimaryKeyRelatedField(many=True, queryset=Habit.objects.all(), allow_null=True)
    duration = serializers.IntegerField(validators=[DurationValidator('duration')])

    class Meta:
        model = Habit
        fields = '__all__'
