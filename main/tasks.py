import requests
from celery import shared_task

from users.models import User


@shared_task
def send_reminder(bot_token, user_id, habit_action):
    base_url = f'https://api.telegram.org/bot{bot_token}'

    user = User.objects.get(pk=user_id)
    chat_id = user.tg_id
    message_text = f'Напоминаю: через 5 минут нужно "{habit_action}"!'
    url = f'{base_url}/sendMessage?chat_id={chat_id}&text={message_text}'

    response = requests.get(url)
    print(response.json())
