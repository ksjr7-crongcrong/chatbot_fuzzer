from flask import Flask
from flask import session, request, render_template, redirect, url_for
from functools import wraps
from lib.chatbot import ChatBot
from pytz import timezone
from datetime import datetime
import requests as req

server = Flask(__name__)
server.secret_key = "7e733a6a61b057024842ca1825409c51a2f80100"
chatbot = None


class ConfGetError(Exception):
    def __init__(self, msg="Config Endpoint does not give config"):
        self.msg = msg

    def __str__(self):
        return self.msg


class TalkGetError(Exception):
    def __init__(self, msg="Talk Endpoint does not give reply"):
        self.msg = msg

    def __str__(self):
        return self.msg


class ConfInsufficientError(Exception):
    def __init__(self, msg="Config Endpoint does omitted some config"):
        self.msg = msg

    def __str__(self):
        return self.msg


@server.route('/', methods=['GET'])
def main():
    return render_template('index.html')


@server.route('/auto_check', methods=['POST'])
def auto_check():
    """
    시작 화면에서 넘겨받은 인자를 통해 검사를 진행합니다.
    """
    api_url = request.form.get('api_url')
    check_list = request.form.getlist('category')
    check_str = "|".join(check_list)
    return render_template('auto_check.html', check_list=check_list, check_str=check_str)

@server.route('/check/<category>', methods=['GET'])
def check(category):
    """
    category에 해당하는 검사를 진행 후 결과를 반환합니다.
    """
    return {"status": "success"}


@server.route('/api_valid_check', methods=['POST'])
def api_valid_check():
    global chatbot
    """
    API 페이지의 유효성을 검사합니다.
    1. conf endpoint 결과 값 존재 여부 검사
    2. conf endpoint 결과 값 내에 interval 값 존재 여부 검사
    3. talk endpoint 결과 값 존재 여부 검사
    """
    params = request.get_json()
    if 'api_url' not in params:
        return {"status": "error", "msg": "API URL does not sent"}
    api_url = params['api_url']
    if not api_url:
        return {"status": "error", "msg": "Empty API URL"}
    try:
        if api_url.endswith("/"):
            api_url = api_url[:-1]
        with req.Session() as s:
            r = s.get(api_url+"/conf")
            conf_data = r.json()
            if conf_data == "":
                raise ConfGetError()

            if "interval" not in conf_data:
                raise ConfInsufficientError()

            data = {"msg": "check message"}
            r = s.post(api_url+"/talk", data=data)
            talk_data = r.json()
            if talk_data == "":
                raise TalkGetError()
        chatbot = ChatBot(api_url)
        return {"status": "success", "msg": "API is valid"}
    except req.exceptions.Timeout:
        return {"status": "error", "msg": "Timeout"}
    except req.exceptions.ConnectionError:
        return {"status": "error", "msg": "Connection Error"}
    except req.exceptions.RequestException as e:
        return {"status": "error", "msg": "Request Error"}
    except ConfGetError:
        return {"status": "error", "msg": ConfGetError}
    except ConfInsufficientError:
        return {"status": "error", "msg": ConfInsufficientError}
    except TalkGetError:
        return {"status": "error", "msg": TalkGetError}
    except Exception as e:
        return {"status": "error", "msg": "Unknown Error"}


@server.route('/flag', methods=['GET'])
def flag():
    return {"flag": "This_SERVICE_is_NOT_CTF_Prob!!!!!!!!!!!"}


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)
