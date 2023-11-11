from django.db import models
from rest_framework.exceptions import ValidationError

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class HabitType(models.TextChoices):
    useful = 'useful'
    pleasant = 'pleasant'


class Frequency(models.TextChoices):
    daily = 'daily'
    once_every_two_days = 'once_every_two_days'
    once_every_three_days = 'once_every_three_days'
    once_every_four_days = 'once_every_four_days'
    once_every_five_days = 'once_every_five_days'
    once_every_six_days = 'once_every_six_days'
    weekly = 'weekly'


def validate_related_habits_with_reward(value):
    if value.related_habits.exists() and value.reward:
        raise ValidationError('Cannot choose both related habits and a reward')


def validate_related_habits_type(value):
    if value.related_habits.filter(habit_type=HabitType.useful):
        raise ValidationError('Related habits cannot be of type "useful"')


def validate_pleasant_habit(value):
    if value.habit_type == HabitType.pleasant and (value.reward.exists() or value.related_habits):
        raise ValidationError('Pleasant habbit cannot have reward or related_habbits')


class Habit(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    place = models.CharField(max_length=50, verbose_name='Место')
    time = models.TimeField(verbose_name='Время')
    action = models.CharField(max_length=200, verbose_name='Действие')
    habit_type = models.CharField(max_length=8, choices=HabitType.choices, default=HabitType.useful,
                                  verbose_name='Тип привычки')
    related_habits = models.ManyToManyField('self', symmetrical=False, related_name='habits',
                                            verbose_name='Связанные привычки', blank=True)
    frequency = models.CharField(max_length=21, choices=Frequency.choices, default=Frequency.daily,
                                 verbose_name='Периодичность')
    reward = models.CharField(max_length=150, verbose_name='Вознаграждение', **NULLABLE)
    duration = models.SmallIntegerField(verbose_name='Длительность выполнения')
    is_public = models.BooleanField(default=False, verbose_name='Опубликовано')

    def __str__(self):
        return f'Привычка: {self.action[:20]}, принадлежит user:{self.owner}'

    def clean(self):
        validate_related_habits_with_reward(self)
        validate_related_habits_type(self)
        validate_pleasant_habit(self)

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
