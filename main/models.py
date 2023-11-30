import json
from datetime import timedelta, datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from config.settings import tg_token
from users.models import User

bot_token = tg_token

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
        return f'Привычка: {self.action[:20]}, принадлежит user:{self.owner.tg_username}'

    def create_reminder_task(self):
        interval = None

        if self.frequency == Frequency.daily:
            interval = 1
        elif self.frequency == Frequency.once_every_two_days:
            interval = 2
        elif self.frequency == Frequency.once_every_three_days:
            interval = 3
        elif self.frequency == Frequency.once_every_four_days:
            interval = 4
        elif self.frequency == Frequency.once_every_five_days:
            interval = 5
        elif self.frequency == Frequency.once_every_six_days:
            interval = 6
        elif self.frequency == Frequency.weekly:
            interval = 7

        habit_time = self.time
        current_date = datetime.now().date()

        start_time = datetime.combine(current_date, habit_time) - timedelta(minutes=5)

        interval_schedule = IntervalSchedule.objects.create(
            every=interval,
            period=IntervalSchedule.DAYS,
        )

        try:
            periodic_task, created = PeriodicTask.objects.get_or_create(
                interval=interval_schedule,
                name=f'Reminder for habit {self.id}',
                task='main.tasks.send_reminder',
                args=json.dumps([bot_token, self.owner.id, self.action]),
                start_time=start_time,
            )
        except ObjectDoesNotExist as e:
            print(f"Error creating periodic task: {e}")
            return

        if not created:
            periodic_task.enabled = False
            periodic_task.save()
            periodic_task.delete()

            self.create_reminder_task()

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
