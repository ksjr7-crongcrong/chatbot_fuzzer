from telethon import TelegramClient
from time import sleep
from lib.chatbot_communicator import AsyncChatbotCommunicator
from config import config
telegram = config['telegram']

class TelegramCommunicator(AsyncChatbotCommunicator):

    def __init__(self, bot_info):
        self.start_idx = 0
        self.bot_id = 0
        telegram['BOTNAME'] = bot_info['name']
        
    async def send_questions(self, q_list):
        bot = TelegramClient('session', telegram['API_ID'], telegram['API_HASH'])
        bot.connect()

        if not bot.is_user_authorized():
            bot.sign_in(telegram['PHONE'], telegram['AUTHCODE'])

        async with bot as client:
            info_msg = await client.send_message(telegram['BOTNAME'], "msg for get current idx")
            self.start_idx = info_msg.id
            self.bot_id = info_msg.to_id.user_id
            sleep(int(telegram['INTERVAL']))
            for q in q_list:
                await client.send_message(telegram['BOTNAME'], q)
                sleep(int(telegram['INTERVAL']))
        

    async def receive_replys(self, q_len):
        bot = TelegramClient('session', telegram['API_ID'], telegram['API_HASH'])
        bot.connect()

        if not bot.is_user_authorized():
            bot.sign_in(telegram['PHONE'], telegram['AUTHCODE'])
        async with bot as client:
            start = self.start_idx + 1 # also remove reply of msg for get idx
            end = start + (q_len * 2) + 10 # give margin to solve unreplyed messages problem
            replys = await client.get_messages(telegram['BOTNAME'], reverse = True, max_id = end, min_id=start)
            all_ans = [m.message for m in replys if m.message is not None and m.sender_id == self.bot_id]
            return all_ans