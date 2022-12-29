from django.core.management.base import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from goals.models import Goal, GoalCategory


class Command(BaseCommand):
    help = 'Runs telegram bot'
    tg_client = TgClient("5713673670:AAGlsWfGCfrVj-DEM4AJjxYFJJQJib1iAAc")
    offset = 0

    def choose_category(self, msg: Message, tg_user: TgUser):
        goal_categories = GoalCategory.objects.filter(
            board__participants__user=tg_user.user,
            is_deleted=False,
        )
        goal_categories_str = '\n'.join(['-' + goal.title for goal in goal_categories])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Выберите категорию:\n {goal_categories_str}')

        is_running =True

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, 'message'):
                    category = goal_categories.filter(title=msg.text)
                    if category:
                        self.create_goal(msg, tg_user, category)
                        is_running = False
                    elif msg.text == '/cancel':
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f'Операция отменена')
                        is_running = False
                    else:
                        self.tg_client.send_message(
                            chat_id=msg.chat.id,
                            text=f'Категории с названием: {msg.text} не существует')
                        is_running = False

    def create_goal(self, msg: Message, tg_user: TgUser, category: GoalCategory):

        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Введите заголовок для названия цели')
        is_running = True

        while is_running:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if item.message == '/cancel':
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f'Операция отменена')
                    is_running = False
                else:
                    goal = Goal.objects.create(
                        category=category,
                        user=tg_user.user,
                        title=item.message.text,
                    )
                    self.tg_client.send_message(
                        chat_id=msg.chat.id,
                        text=f'Цель {goal.title} created')
                    is_running = False

    def get_goals(self, msg: Message, tg_user: TgUser):
        goals = Goal.objects.filter(
            category__board__participants__user=tg_user.user,
        ).exclude(status=Goal.Status.archived)
        goals_str = '\n'.join([goal.title for goal in goals])
        self.tg_client.send_message(
            chat_id=msg.chat.id,
            text=f'Вот список ваших целей:\n {goals_str}'
        )

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
        if msg.text == '/goals':
            self.get_goals(msg, tg_user)
        elif msg.text == '/create':
            self.offset += 1
            self.choose_category(msg, tg_user)
        else:
            self.tg_client.send_message(
                chat_id=msg.chat.id,
                text=f'Неизвестная команда! {msg.text}')

    def handle(self, *args, **options):
        while True:
            res = self.tg_client.get_updates(offset=self.offset)
            for item in res.result:
                self.offset = item.update_id + 1
                if hasattr(item, 'message'):
                    self.handle_message(item.message)