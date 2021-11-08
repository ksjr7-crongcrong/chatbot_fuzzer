from lib.db_manager import DBManager
from lib.fuzz_set_maker import FuzzSetCreator
from lib.analyzer import Analyzer


class Controller:
    def __init__(self):
        self.__data_injector = None
        self.analyzer = Analyzer()
        self.db_manager = DBManager("fuzz_set.db")
        self.q_maker = FuzzSetCreator(self.db_manager.conn)

    def ready_db(self):
        self.q_maker.ready()

    def get_query_list(self, category: str, light: bool = False):
        if light:
            stmt = f"SELECT msg FROM questions WHERE category='{category}' order by id limit 10"
        else:
            stmt = f"SELECT msg FROM questions WHERE category='{category}' order by id"
        q_list = self.db_manager.query(stmt)
        return q_list

    def get_query_len_by_list(self, category_list):
        total_len = 0
        for category in category_list:
            stmt = f"SELECT count() FROM questions WHERE category='{category}'"
            total_len += self.db_manager.query(stmt)
        return total_len

    def check(self, category: str):
        q_list = self.get_query_list(category, light=True)
        if self.__data_injector is not None:
            # Output : [(q, a), ... ]
            raw_result = self.__data_injector.fuzz(q_list)
            # Output : [(q, a), ... ]
            result = self.analyzer.privacy_check(category, raw_result)
            return {'status': 'success', 'result': (len(result), result)}
        return {'status': 'fail'}

    @property
    def data_injector(self):
        return self.__data_injector

    @data_injector.setter
    def data_injector(self, data_injector):
        self.__data_injector = data_injector
