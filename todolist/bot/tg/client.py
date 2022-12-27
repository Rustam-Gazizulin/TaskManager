import requests

from bot.tg import dc


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int=0, timeout: int=60) -> dc.GetUpdatesResponse:
        url = self.get_url('getUpdates')
        response = requests.get(url, params={"offset": offset, "timeout": timeout})
        return dc.GET_UPDATES_SCHEMA.load(response.json())

    def send_message(self, chat_id: int, text: str) -> dc.SendMessageResponse:
        url = self.get_url('sendMessage')
        response = requests.get(url, params={"chat_id": chat_id, "text": text})
        return dc.SEND_MESSAGE_RESPONSE_SCHEMA.load(response.json())

# cl = TgClient("5713673670:AAGlsWfGCfrVj-DEM4AJjxYFJJQJib1iAAc")
# print(cl.get_updates(offset=0, timeout=60))
# print(cl.send_message(chat_id=896458874, text='good'))