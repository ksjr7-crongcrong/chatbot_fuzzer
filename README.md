[contributors-shield]: https://img.shields.io/github/contributors/ksjr7-crongcrong/chatbot_fuzzer?style=flat-square
[contributors-url]: https://github.com/ksjr7-crongcrong/chatbot_fuzzer/graphs/contributors
[license-shield]: https://img.shields.io/github/license/ksjr7-crongcrong/chatbot_fuzzer.svg?style=flat-square
[license-url]: https://github.com/ksjr7-crongcrong/chatbot_fuzzer/blob/main/LICENSE

[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]

## Service Flow

### 시작 화면

client에게 다음 항목을 요청합니다.
- 챗봇과 소통할 수 있는 API 주소
    - 유효성 검사는 API의 conf endpoint에 요청, talk endpoint를 통해 총 2회 검증

client에게 검사에 대해 customizing을 제공합니다.
- 검사받을 카테고리 선택
    - 카테고리를 선택할 때 마다 JS를 활용하여 동적으로 총 예상 시간을 알려줍니다.
- 결과파일 암호화 선택
    - 추가 예정
    - 서버에 챗봇의 응답결과가 남지 않음을 공지
    - 암호화를 하겠다고 할 시 공개키를 요청

### 점검 진행화면

검사 시간이 굉장히 길기 때문에 카테고리 별로 단위를 쪼개어 검사를 진행
async, await 문법을 활용하여 JS를 통해 카테고리마다 검사 완료 여부 표시

### 결과 화면 

중요 지표를 바 그래프 형태로 제공
노출된 개인정보와 해당 답변을 유도한 질문 데이터를 정리한 보고서를 다운받을 수 있도록 제공 ( 엑셀 파일 )

## 아키텍쳐 구조

Flask Web Server + gunicorn(worker:gevent)
- Non-Blocking + 비동기 방식으로 동작

## 챗봇 API 요구 사항
| Endpoint | Req Method | Req Data Type | Req Body | Resp Data Type | Resp Body | comment |
|:--------:|:--------------:|:-----------------:|:------------:|:------------------:|:-------------:|:-------:|
| conf | GET | None | None | json | {"interval":int} | send talk interval |
| talk | POST | json | {"msg":str} | json | {"msg":str} | send Q and receive A |

## How to USE

```bash
pip install -r requirements.txt
gunicorn app:server -k gevent
```
