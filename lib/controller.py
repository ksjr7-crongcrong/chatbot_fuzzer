from lib.db_manager import DBManager
from lib.fuzz_set_maker import FuzzSetCreator
from lib.analyzer import Analyzer
from typing import List, Dict
import json


class Controller:
    def __init__(self):
        self.__data_injector = None
        self.analyzer = Analyzer()
        self.db_manager = DBManager("fuzz_set.db")
        self.q_maker = FuzzSetCreator(self.db_manager.conn)

    def ready_db(self):
        self.q_maker.ready()

    def get_query_list(self, category: str, use_subject: bool = True, use_descriptive: bool = True, light: bool = False):
        stype = 3
        if not use_subject:
            if not use_descriptive:
                stype = 0
            else:
                stype = 1
        else:
            if not use_descriptive:
                stype = 2
        if light:
            stmt = f"SELECT msg FROM questions WHERE category='{category}' and stype={stype} order by id limit 10"
        else:
            stmt = f"SELECT msg FROM questions WHERE category='{category}' and stype={stype} order by id"
        q_list = self.db_manager.query(stmt)
        return q_list

    def get_query_len_by_list(self, category_list, use_subject=True, use_descriptive=True):
        stype = 3
        if not use_subject:
            if not use_descriptive:
                stype = 0
            else:
                stype = 1
        else:
            if not use_descriptive:
                stype = 2
        total_len = 0
        for category in category_list:
            stmt = f"SELECT count() FROM questions WHERE category='{category}' and stype={stype}"
            total_len += self.db_manager.query(stmt)
        return total_len

    def parse_result(self, check_list: list, full_list: Dict[str, List[str]], use_subject: bool = True, use_descriptive: bool = True):
        result_data = {}
        category_eng2kor = {
            "rrn": "주민등록번호",
            "phone": "휴대전화번호",
            "number": "집전화번호",
            "bank": "계좌번호",
            "credit": "신용카드번호",
            "health": "건강보험번호",
            "email": "이메일 주소",
            "addr": "주소",
            "drive": "운전면허번호",
            "passport": "여권번호"
        }
        privacy_level = {
            "high": ["rrn", "passport", "drive"],
            "medium": ["bank", "credit"],
            "low": ["health", "addr", "phone", "number", "email"]
        }
        result = {
            'level_count': {'high': 0, 'medium': 0, 'low': 0},
            'checked_category': [],
            'category_detected_cnt': {},
        }
        total_len = self.get_query_len_by_list(
            check_list, use_subject, use_descriptive)
        result['checked_category'] = check_list
        full_result = {}
        detected_count = {}
        for category in full_list:
            count, _result = full_list[category]
            full_result[category_eng2kor[category]] = _result
            detected_count[category] = count
        result['category_detected_cnt'] = detected_count
        result['level_count']['high'] = sum(
            detected_count[key] for key in detected_count if key in privacy_level["high"])
        result['level_count']['medium'] = sum(
            detected_count[key] for key in detected_count if key in privacy_level["medium"])
        result['level_count']['low'] = sum(
            detected_count[key] for key in detected_count if key in privacy_level["low"])
        full_result_list = []
        for c in full_result:
            for row in full_result[c]:
                q, a = row
                level = "주의"
                if c in privacy_level["high"]:
                    level = "위험"
                full_result_list.append(
                    {"category": c, "q": q, "a": a, "level": level})
        top_result = full_result_list[:5]

        result_data['top'] = top_result
        result_data['total_queryed'] = total_len
        result_data['total_detected'] = sum(detected_count.values())
        result_data['json'] = json.dumps(result)
        result_data['high_cnt'] = result['level_count']['high']
        return result_data

    def check(self, category: str, use_subject: bool = True, use_descriptive: bool = True):
        q_list = self.get_query_list(
            category, use_subject, use_descriptive, light=True)
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
