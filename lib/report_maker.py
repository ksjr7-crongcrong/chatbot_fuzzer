import pandas as pd
from typing import List, Dict, Any
from datetime import datetime
import pytz

tz_KR = pytz.timezone("Asia/Seoul")

def make_report(data: List[Dict[str, Any]], report_path:str) -> str:
    key_eng2kor = {
        "category": "카테고리",
        "q": "질문",
        "a": "답변",
        "level": "위험도"
    }
    
    cur_kr_time = datetime.now(tz_KR).strftime("%y%m%d-%H%M%S")

    df = pd.DataFrame.from_dict(data)
    df.rename(columns = key_eng2kor, inplace=True)

    if not report_path[:-1] == "/":
        report_path += "/"
    
    df.to_excel(report_path + cur_kr_time + '.xlsx', index=False)
    
    return cur_kr_time