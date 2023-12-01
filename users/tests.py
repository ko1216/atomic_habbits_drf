from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from users.models import User
from users.serializers import UserSerializer, RegisterSerializer


class TestRegisterAPICase(APITestCase):
    def setUp(self) -> None:
        self.user1 = User.objects.create(
            tg_id=42425,
            tg_username='user1000',
        )

        self.user_to_create_valid = {
            'tg_id': 4634,
            'tg_username': 'user1000',
            'password': 'password'
        }

        self.user_to_create = {
            'tg_id': 4634,
            'tg_username': 'user100',
            'password': 'password'
        }

        self.user_to_create_noname = {
            'tg_id': 4634,
            'password': 'password'
        }

    def test_create_200(self):
        response = self.client.post(reverse('users:register'), self.user_to_create)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                'user': response.json()['user'],
                'message':
                    'User created successfully. Now perform Login to get your token'
            }
        )

    def test_create_valid(self):
        response = self.client.post(reverse('users:register'), self.user_to_create_valid)

        self.assertEqual(
            response.json(),
            {'tg_username': ['user with this Ник в тг already exists.']}

        )
