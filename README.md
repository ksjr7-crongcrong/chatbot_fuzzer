# 구성도

추가예정

## 다양한 챗봇 지원 고려

### chatbot api의 소통 방법 고려하여 추상클래스 설계
챗 봇에게 메시지를 보내고 답변을 받아오는 부분 추상화
동기, 비동기 방식 고려 두가지 추상 클래스로 나누어 설계
- AsyncChatbotCommunicator
- SyncChatbotCommunicator

## config
chatbot 별로 config를 저장할 수 있게 설계

### TELEGRAM
- API_ID, API_HASH : Telethon
- BOTNAME : Fuzzing Target
- INTERVAL : msg send interval

## qna_parser
- add_tag : 질문 유형에 대한 tag를 해당 질문의 답변에 붙이는 루틴

## How to USE

### require
```bash
pip install -r requirements.txt
```

이 후 chatbot.ini 파일에 사전정보를 넣어줍니다.
AUTHCODE는 안넣어도도 됩니다 ( 실행 시 요청할 겁니다. )

### run
```
python main.py
```

### QnA
- Q: 너무 느려요
    - A: INTERVAL을 줄이세요, 다만 너무 짧은 INTERVAL은 챗봇 측이 사용자를 ban할 수 있습니다.
