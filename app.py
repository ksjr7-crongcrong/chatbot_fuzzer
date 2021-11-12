"""
:TO DO:

모든 check가 완료되었는지를 알 수 있도록 루틴을 wrapper로 만들고 show_result 호출시마다 체크하도록 하기
사유 : f5 누르면 다시 체크하라고 하는것도 아니고 그냥 데이터가 없는채로 나옴
"""
from flask import Flask
from flask import session, request, render_template, redirect, url_for
from functools import wraps
from lib.chatbot import ChatBot
from lib.controller import Controller
from lib.data_injector import DataInjector
from lib.exception import *
from pytz import timezone
from datetime import datetime
import requests as req
import uuid
from lib.data_injector import DataInjector
from functools import reduce

server = Flask(__name__)
server.secret_key = "7e733a6a61b057024842ca1825409c51a2f80100"
chatbot = None
controller = Controller()
controller.ready_db()
resultQ = {}


@server.route('/', methods=['GET'])
def main():
    session['uid'] = str(uuid.uuid4())
    return render_template('index.html')


@server.route('/show_progress', methods=['POST'])
def show_progress():
    """
    시작 화면에서 넘겨받은 인자를 통해 검사를 진행합니다.
    """
    api_url = request.form.get('api_url')
    check_list = request.form.getlist('category')
    session['check_list'] = check_list
    check_str = "|".join(check_list)
    return render_template('progress.html', check_list=check_list, check_str=check_str)


@server.route('/check/<category>', methods=['GET'])
def check(category):
    """
    category에 해당하는 검사를 진행 후 결과를 반환합니다.
    """
    result = controller.check(category)
    if result['status'] == "success":
        resultQ[session['uid']+category] = result['result']
    return {"status":result['status']}

@server.route('/show_result', methods=['GET'])
def show_result():
    """
    결과를 보여주는 페이지
    """
    privacy_level = {"high":["rrn", "passport", "drive", "bank", "credit", "health"], "medium":["addr", "phone", "number", "email"], "low":[]}
    if "check_list" not in session:
        return {"total queryed":0, "result": "Non check executed"}
    check_list = session['check_list']
    total_len = controller.get_query_len_by_list(check_list)
    full_result = {}
    detected_count = {}
    for category in check_list:
        key = session['uid']+category
        if key in resultQ:
            count, result = resultQ[key]
            del resultQ[key]
            full_result[category] = result
            detected_count[category] = count
    high_level_count = sum(detected_count[key] for key in detected_count if key in privacy_level["high"])
    medium_level_count = sum(detected_count[key] for key in detected_count if key in privacy_level["medium"])
    full_result_list = []
    for c in full_result:
        for row in full_result[c]:
            q, a = row
            level = "주의"
            if c in privacy_level["high"]:
                level = "위험"
            full_result_list.append({"category":c, "q":q, "a":a, "level":level})
    top_result = full_result_list[:5]
    return render_template('charts.html',
        check_list = "|".join(check_list),
        value_list = "|".join([str(detected_count[c]) for c in check_list if c in detected_count]),
        level_count = f'{high_level_count}|{medium_level_count}',
        top_result = top_result,
        total_queryed = total_len,
        total_detected = sum(detected_count.values()),
        high_level_count = high_level_count
    )

@server.route('/api_valid_check', methods=['POST'])
def api_valid_check():
    """
    API 페이지의 유효성을 검사합니다.
    1. conf endpoint 결과 값 존재 여부 검사
    2. conf endpoint 결과 값 내에 interval 값 존재 여부 검사
    3. talk endpoint 결과 값 존재 여부 검사
    """
    global chatbot
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
            r = s.post(api_url+"/talk", json=data)
            talk_data = r.json()
            if talk_data == "":
                raise TalkGetError()
        chatbot = ChatBot(api_url)
        data_injector = DataInjector(chatbot)
        controller.data_injector = data_injector
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
    return render_template('charts.html')
    return {"flag": "This_SERVICE_is_NOT_CTF_Prob!!!!!!!!!!!"}


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)
