from django.urls import path

from main.apps import MainConfig
from main.views import HabitListAPIView, HabitRetrieveAPIView, HabitCreateAPIView, HabitUpdateAPIView, \
    HabitDestroyAPIView, PublicHabitListAPIView

app_name = MainConfig.name

urlpatterns = [
    path('habits/', HabitListAPIView.as_view(), name='habits'),
    path('public_habits/', PublicHabitListAPIView.as_view(), name='public_habits'),
    path('habit/<int:pk>', HabitRetrieveAPIView.as_view(), name='habit'),
    path('habit/create/', HabitCreateAPIView.as_view(), name='habit_create'),
    path('habit/update/<int:pk>', HabitUpdateAPIView.as_view(), name='habit_update'),
    path('habit/delete/<int:pk>', HabitDestroyAPIView.as_view(), name='habit_delete')
]
