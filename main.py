from lib.db_manager import DBManager
from fuzz_set_maker import FuzzSetCreator
from regexp_checker import match
from telegram_manager import TelegramCommunicator

class ChatbotFuzzer:
    def __init__(self, chatbot_communicator):
        self.chatbot_communicator = chatbot_communicator
        self.db_manager = DBManager("fuzz_set.db")
        self.db_conn = self.db_manager.conn
        FuzzSetCreator(self.db_conn).ready()
    
    def get_fuzz_set(self) -> list:
        fuzz_set = []
        fuzz_set_cursor = self.db_conn.execute("SELECT msg FROM questions order by id")
        for row in fuzz_set_cursor:
            fuzz_set.append(row[0])
        return fuzz_set

    def get_category_iter(self) -> list:
        fuzz_set_category_iter = []
        fuzz_set_cursor = self.db_conn.execute("SELECT category FROM questions order by id")
        for row in fuzz_set_cursor:
            fuzz_set_category_iter.append(row[0])
        return fuzz_set_category_iter

    def add_tag(self, category_iter, chatbot_response):
        return list(zip(category_iter, chatbot_response))

    def analyze_answer(self, tagged_answer) -> dict:
        result = {}
        for category, answer in tagged_answer:
            exist_privacy = match(category, answer)
            if exist_privacy:
                result[category] = answer
        return result

    def fuzz(self) -> dict:
        _, chatbot_response = self.chatbot_communicator.talk(self.get_fuzz_set())
        fuzz_set_category_iter = self.get_category_iter()
        tagged_answer = self.add_tag(fuzz_set_category_iter, chatbot_response)
        result = self.analyze_answer(tagged_answer)
        return result

if __name__ == "__main__":
    telegram = TelegramCommunicator({"name":"crongcrong_bot"})
    fuzzer = ChatbotFuzzer(telegram)
    fuzz_result = fuzzer.fuzz()
    print(fuzz_result)