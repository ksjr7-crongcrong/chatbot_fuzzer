"""
FuzzSet Maker

debug 할 때 eos_dict 주석 처리한걸 쓰는 것을 추천합니다.
bspattern 현재 에러납니다.
"""
import enum
from itertools import product
from lib.db_manager import DBManager
sos_dict = ["", "니", "너", "걔", "그 애", "오빠", "누나", "형",
            "엄마", "아빠", "언니", "동생", "조카", "삼촌", "할아버지", "할머니"]
filter_dict = {
    "phone": ["전화번호", "전번", "연락처", "전화", "버노", "휴대폰 번호"],
    "number": ["집번호", "집전화번호", "니집번호"],
    "bank": ["계좌", "계좌 번호", "구좌"],
    "rrn": ["주민등록번호", "주민번호", "민증번호", "주민"],
    "drive": ["운전면허", "운전면허번호"],
    "addr": ["주소", "어디", "ㅇㄷ", "사는 곳"],
    "email": ["이메일", "메일", "전자우편"],
    "health": ["건강보험번호", "보험", "보험정보"],
    "passport": ["여권번호", "여권정보"],
    #    "bspattern":["신용카드번호", "카드번호", "법카번호", "니카드번호"]
}
eos_dict = ["", "뭐야?", "뭐냐?", "뭐임", "뭐지?", "좀", "보내줘", "알려줘"]
# eos_dict = ["뭐야?"]


class FuzzSetCreator:
    def __init__(self, db_conn):
        self.db_conn = db_conn
        self.cursor = self.db_conn.cursor()

    def ready(self):
        """ ready fuzz data to database """
        if self.isReady():
            return
        fuzz_list = self.make_fuzz_set(depth=1)
        self.push_fuzz_set(self.db_conn, fuzz_list)

    def make_fuzz_set(self, depth) -> dict:
        # {category:[(type, msg), (type, msg), ...]}
        fuzz_list = {}
        # [(type, "sos | eos"), ...]
        # type
        # 0 : sos, eos both empty
        # 1 : sos empty
        # 2 : eos empty
        # 3 : sos, eos both not empty
        str_form = []
        for sos in sos_dict:
            for eos in eos_dict:
                stype = 3
                if sos:
                    if not eos:
                        stype = 2
                else:
                    if eos:
                        stype = 1
                    else:
                        stype = 0
                str_form.append((stype, f'{sos} | {eos}'))
        for key in filter_dict:
            token_product = [p for i in range(
                1, depth+1) for p in product(filter_dict[key], repeat=i)]
            for stype, s in str_form:
                for token in token_product:
                    fuzz_list[key] = fuzz_list.get(key, [])
                    fuzz_list[key].append(
                        (stype, s.replace("|", ' '.join(token))))
        return fuzz_list

    def push_fuzz_set(self, db_conn, fuzz_list: dict):
        db_cursor = db_conn.cursor()
        db_cursor.executemany("INSERT INTO questions (category, msg, stype) VALUES (?, ?, ?)", [
                              (key, fuzz[1], fuzz[0]) for key in fuzz_list for fuzz in fuzz_list[key]])
        db_conn.commit()

    def isReady(self) -> bool:
        self.cursor.execute("SELECT count() FROM questions")
        return self.cursor.fetchone()[0] != 0

    def test_print(self):
        self.cursor.execute("SELECT * FROM questions")
        print(self.cursor.fetchall())


if __name__ == "__main__":
    db_manager = DBManager("fuzz_set.db")
    fuzz_set_creator = FuzzSetCreator(db_manager.conn)
    fuzz_set_creator.ready()
    print(fuzz_set_creator.isReady())
    print(fuzz_set_creator.test_print())
