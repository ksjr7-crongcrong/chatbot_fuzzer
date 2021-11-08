from typing import List, Tuple
from lib.regexp_checker import match


class Analyzer:
    def __init__(self) -> None:
        pass

    def privacy_check(self, category: str,  raw_result: List[Tuple[str, str]]) -> List[Tuple[str, str]]:
        unmasked_privacy = []
        for q, a in raw_result:
            exist_privacy = match(category, a)
            if exist_privacy:
                unmasked_privacy.append((q, a))
        return unmasked_privacy
