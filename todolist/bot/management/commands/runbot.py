from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient("5713673670:AAGlsWfGCfrVj-DEM4AJjxYFJJQJib1iAAc")

    def handle_message(self, msg: Message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=msg.msg_from.id,
            tg_chat_id=msg.chat.id,)
        if created:
            tg_user.generate_verification_code()
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Подтвердите свой аккаунт!'
                    f'Для подтверждения необходимо ввести код: {tg_user.verification_code} на сайте'
            )
        elif msg.text == '/goals':
            goals = Goal.objects.filter(
                category__board__participants__user=tg_user.user,
            ).exclude(status=Goal.Status.archived)
            #goals_list = [goal.title for goal in goals]
            goals_str = '\n'.join([goal.title for goal in goals])
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Вот список ваших целей:\n {goals_str}'
            )



    def handle(self, *args, **options):
        offset = 0
        while True:
            res = self.tg_client.get_updates(offset=offset)
            for item in res.result:
                offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)