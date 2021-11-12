from typing import List, Tuple
from time import sleep


class DataInjector:
    def __init__(self, target) -> None:
        self.target = target

    def fuzz(self, q_list: list) -> List[Tuple[str, str]]:
        raw_result = []
        for q in q_list:
            a = self.target.talk(q)
            raw_result.append((q, a))
        return raw_result
