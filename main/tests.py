from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from main.models import Habit, HabitType
from users.models import User


class PublicHabitListTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(
            tg_id=6634345,
            tg_username='name10'
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user,
            place='Дома',
            time='12:00:00',
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            reward='Яблоко',
            duration=60,
            is_public=True,
        )

        self.useful_habit_2 = Habit.objects.create(
            owner=self.user,
            place='Дома',
            time='10:00:00',
            action='Зарядка',
            reward='Молоко',
            duration=60,
            is_public=False,
        )

        self.useful_habit_4 = Habit.objects.create(
            owner=self.user,
            place='Дома',
            time='16:00:00',
            action='Упражнения',
            duration=60,
            is_public=True
        )

        self.pleasant_habit.related_habits.set([self.useful_habit_4])
        self.useful_habit_4.related_habits.set([self.pleasant_habit])

    def test_get(self):

        self.client.force_authenticate(user=self.user)

        response = self.client.get(reverse('main:public_habits'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                "count": 3,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.pleasant_habit.id,
                        "owner": self.user.id,
                        "place": self.pleasant_habit.place,
                        "time": self.pleasant_habit.time,
                        "action": self.pleasant_habit.action,
                        "habit_type": self.useful_habit_4.habit_type.value,
                        "related_habits": [self.useful_habit_4.id],
                        "frequency": self.pleasant_habit.frequency.value,
                        "reward": self.pleasant_habit.reward,
                        "duration": self.pleasant_habit.duration,
                        "is_public": self.pleasant_habit.is_public
                    },
                    {
                        "id": self.useful_habit_1.id,
                        "owner": self.user.id,
                        "place": self.useful_habit_1.place,
                        "time": self.useful_habit_1.time,
                        "action": self.useful_habit_1.action,
                        "habit_type": self.useful_habit_1.habit_type.value,
                        "related_habits": [],
                        "frequency": self.useful_habit_1.frequency.value,
                        "reward": self.useful_habit_1.reward,
                        "duration": self.useful_habit_1.duration,
                        "is_public": self.useful_habit_1.is_public
                    },
                    {
                        "id": self.useful_habit_4.id,
                        "owner": self.user.id,
                        "place": self.useful_habit_4.place,
                        "time": self.useful_habit_4.time,
                        "action": self.useful_habit_4.action,
                        "habit_type": self.useful_habit_4.habit_type.value,
                        "related_habits": [self.pleasant_habit.id],
                        "frequency": self.useful_habit_4.frequency.value,
                        "reward": self.useful_habit_4.reward,
                        "duration": self.useful_habit_4.duration,
                        "is_public": self.useful_habit_4.is_public
                    }
                ]
            }
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('main:public_habits'))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )


class HabitListTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            tg_id=6634345,
            tg_username='name3'
        )

        self.user_2 = User.objects.create(
            tg_id=663434501,
            tg_username='name4'
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='12:00:00',
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user_2,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            reward='Яблоко',
            duration=60,
            is_public=True,
        )

        self.useful_habit_2 = Habit.objects.create(
            owner=self.user_2,
            place='Дома',
            time='10:00:00',
            action='Зарядка',
            reward='Молоко',
            duration=60,
            is_public=False,
        )

        self.useful_habit_4 = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='16:00:00',
            action='Упражнения',
            duration=60,
            is_public=True
        )

        self.pleasant_habit.related_habits.set([self.useful_habit_4])
        self.useful_habit_4.related_habits.set([self.pleasant_habit])

    def test_get(self):

        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(reverse('main:habits'))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                "count": 2,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": self.pleasant_habit.id,
                        "owner": self.user_1.id,
                        "place": self.pleasant_habit.place,
                        "time": self.pleasant_habit.time,
                        "action": self.pleasant_habit.action,
                        "habit_type": self.useful_habit_4.habit_type.value,
                        "related_habits": [self.useful_habit_4.id],
                        "frequency": self.pleasant_habit.frequency.value,
                        "reward": self.pleasant_habit.reward,
                        "duration": self.pleasant_habit.duration,
                        "is_public": self.pleasant_habit.is_public
                    },
                    {
                        "id": self.useful_habit_4.id,
                        "owner": self.user_1.id,
                        "place": self.useful_habit_4.place,
                        "time": self.useful_habit_4.time,
                        "action": self.useful_habit_4.action,
                        "habit_type": self.useful_habit_4.habit_type.value,
                        "related_habits": [self.pleasant_habit.id],
                        "frequency": self.useful_habit_4.frequency.value,
                        "reward": self.useful_habit_4.reward,
                        "duration": self.useful_habit_4.duration,
                        "is_public": self.useful_habit_4.is_public
                    }
                ]
            }
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('main:habits'))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )


class HabitRetrieveTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            tg_id=6634345,
            tg_username='name1'
        )

        self.user_2 = User.objects.create(
            tg_id=663434501,
            tg_username='name2'
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='12:00:00',
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user_2,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            reward='Яблоко',
            duration=60,
            is_public=True,
        )

        self.useful_habit_2 = Habit.objects.create(
            owner=self.user_2,
            place='Дома',
            time='10:00:00',
            action='Зарядка',
            reward='Молоко',
            duration=60,
            is_public=False,
        )

        self.useful_habit_4 = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='16:00:00',
            action='Упражнения',
            duration=60,
            is_public=True
        )

        self.pleasant_habit.related_habits.set([self.useful_habit_4])
        self.useful_habit_4.related_habits.set([self.pleasant_habit])

    def test_get(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(reverse('main:habit', kwargs={'pk': self.useful_habit_4.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": self.useful_habit_4.id,
                "owner": self.user_1.id,
                "place": self.useful_habit_4.place,
                "time": self.useful_habit_4.time,
                "action": self.useful_habit_4.action,
                "habit_type": self.useful_habit_4.habit_type.value,
                "related_habits": [self.pleasant_habit.id],
                "frequency": self.useful_habit_4.frequency.value,
                "reward": self.useful_habit_4.reward,
                "duration": self.useful_habit_4.duration,
                "is_public": self.useful_habit_4.is_public
            }
        )

    def test_not_owner(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.get(reverse('main:habit', kwargs={'pk': self.useful_habit_2.pk}))

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем этой записи"
            }
        )

    def test_not_authenticated(self):
        response = self.client.get(reverse('main:habit', kwargs={'pk': self.useful_habit_2.pk}))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )


class HabitCreateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            tg_id=6634345,
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='12:00:00',
            habit_type=HabitType.pleasant,
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            duration=60,
            is_public=True
        )

        self.useful_habit_4 = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_rew_relation = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.pleasant_habit.pk],
            'reward': 'яблоко',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_with_useful_related_habit = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.useful_habit_1.pk],
            'duration': 60,
            'is_public': True
        }

        self.pleasant_habit_valid_with_any = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'related_habits': [self.pleasant_habit.pk],
            'duration': 60,
            'is_public': True
        }

        self.habit_duration_0 = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 0,
            'is_public': True
        }

        self.habit_duration_121= {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 121,
            'is_public': True
        }

    def test_not_authenticated(self):
        response = self.client.get(reverse('main:habit_create'))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )

    def test_create_useful_201(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.useful_habit_4
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.maxDiff = None
        self.assertEqual(
            response.json(),
            {
                "id": 3,
                "owner": self.user_1.id,
                "place": self.useful_habit_4['place'],
                "time": self.useful_habit_4['time'],
                "action": self.useful_habit_4['action'],
                "habit_type": 'useful',
                "related_habits": [],
                "reward": None,
                "frequency": 'daily',
                "duration": self.useful_habit_4['duration'],
                "is_public": self.useful_habit_4['is_public']
            }
        )

    def test_validate_related_habits_with_reward(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.useful_habit_valid_rew_relation
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'detail': [
                    'Cannot choose both related habits and a reward'
                ]
            }
        )

    def test_validate_related_habits_type(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.useful_habit_valid_with_useful_related_habit
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'detail': [
                     'Related habits cannot be of type "useful"'
                ]
            }
        )

    def test_validate_pleasant_habit(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.pleasant_habit_valid_with_any
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {
                'detail': [
                    'Pleasant habbit cannot have reward or related_habbits'
                ]
            }
        )

    def test_valid_duration_less_than_1(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.habit_duration_0
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'duration': ['Duration cannot be less than 1 second']}
        )

    def test_valid_duration_more_than_120(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.post(
            reverse('main:habit_create'),
            self.habit_duration_121
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        self.assertEqual(
            response.json(),
            {'duration': ['Duration must be more than 120 seconds']}
        )


class HabitUpdateTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            tg_id=6634345,
        )

        self.user_2 = User.objects.create(
            tg_id=6634346,
            tg_username='user'
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='12:00:00',
            habit_type=HabitType.pleasant,
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            duration=60,
            is_public=True
        )

        self.useful_habit_4 = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_rew_relation = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.pleasant_habit.pk],
            'reward': 'яблоко',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_with_useful_related_habit = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.useful_habit_1.pk],
            'duration': 60,
            'is_public': True
        }

        self.pleasant_habit_valid_with_any = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'related_habits': [self.pleasant_habit.pk],
            'duration': 60,
            'is_public': True
        }

        self.habit_duration_0 = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 0,
            'is_public': True
        }

        self.habit_duration_121 = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 121,
            'is_public': True
        }

    def test_update_by_non_authorized(self):
        response = self.client.patch(reverse('main:habit_update', kwargs={'pk': self.useful_habit_1.pk}))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )

    def test_not_owner(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.patch(reverse('main:habit_update', kwargs={'pk': self.useful_habit_1.pk}))

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем этой записи"
            }
        )

    def test_update_by_owner(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.patch(reverse('main:habit_update', kwargs={'pk': self.useful_habit_1.pk}),
                                     {"place": "В другом месте"})

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 47,
                "owner": self.user_1.id,
                "place": "В другом месте",
                "time": self.useful_habit_1.time,
                "action": self.useful_habit_1.action,
                "habit_type": 'useful',
                "related_habits": [],
                "reward": None,
                "frequency": 'daily',
                "duration": self.useful_habit_1.duration,
                "is_public": self.useful_habit_1.is_public
            }
        )


class HabitDestroyTestCase(APITestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(
            tg_id=6634345,
        )

        self.user_2 = User.objects.create(
            tg_id=6634345,
            tg_username='test3'
        )

        self.pleasant_habit = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='12:00:00',
            habit_type=HabitType.pleasant,
            action='Посмотреть обучающие тиктоки',
            duration=60,
            is_public=True,
        )

        self.useful_habit_1 = Habit.objects.create(
            owner=self.user_1,
            place='Дома',
            time='16:00:00',
            action='Разминка',
            duration=60,
            is_public=True
        )

        self.useful_habit_4 = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_rew_relation = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.pleasant_habit.pk],
            'reward': 'яблоко',
            'duration': 60,
            'is_public': True
        }

        self.useful_habit_valid_with_useful_related_habit = {
            'owner': self.user_1.pk,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Упражнения',
            'related_habits': [self.useful_habit_1.pk],
            'duration': 60,
            'is_public': True
        }

        self.pleasant_habit_valid_with_any = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'related_habits': [self.pleasant_habit.pk],
            'duration': 60,
            'is_public': True
        }

        self.habit_duration_0 = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 0,
            'is_public': True
        }

        self.habit_duration_121 = {
            'owner': self.user_1.pk,
            'habit_type': HabitType.pleasant,
            'place': 'Дома',
            'time': '16:00:00',
            'action': 'Приятно',
            'duration': 121,
            'is_public': True
        }

    def test_update_by_non_authorized(self):
        response = self.client.get(reverse('main:habit_delete', kwargs={'pk': self.useful_habit_1.pk}))

        self.assertEqual(
            response.json(),
            {
                'detail': 'Authentication credentials were not provided.'
            }
        )

    def test_not_owner(self):
        self.client.force_authenticate(user=self.user_2)

        response = self.client.delete(reverse('main:habit_delete', kwargs={'pk': self.useful_habit_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Вы не являетесь владельцем этой записи"
            }
        )

    def test_update_by_owner(self):
        self.client.force_authenticate(user=self.user_1)

        response = self.client.delete(reverse('main:habit_delete', kwargs={'pk': self.useful_habit_1.pk}))

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
