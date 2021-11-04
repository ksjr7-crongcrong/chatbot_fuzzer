"""
Abstract Layer
Implement this to communicate with chatbot
"""
from abc import *
import asyncio


class AsyncChatbotCommunicator(metaclass=ABCMeta):
    @abstractmethod
    async def send_questions(self, q_list:list):
        pass

    @abstractmethod
    async def receive_replys(self, q_len:int) -> list:
        pass
    
    # return (status_code, replys)
    # status code : 0 is normal, non zero is exception
    # example of exception : Reply count doesn't match to Question count
    def talk(self, q_list) -> tuple:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.send_questions(q_list))
        out = loop.run_until_complete(self.receive_replys(len(q_list)))
        return len(out)-len(q_list), out

class SyncChatbotCommunicator(metaclass=ABCMeta):
    @abstractmethod
    def send_questions(self, q_list):
        pass

    @abstractmethod
    def receive_replys(self, q_len) -> list:
        pass

    def talk(self, q_list) -> list:
        pass