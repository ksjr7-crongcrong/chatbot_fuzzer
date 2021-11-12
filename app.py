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


def fuzzed_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'fuzzed' not in session:
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return wrapper


def param_check(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'check_list' not in session:
            return redirect(url_for('main'))
        return f(*args, **kwargs)
    return wrapper


@server.route('/', methods=['GET'])
def main():
    session['use_subject'] = False
    session['use_descriptive'] = False
    session['check_list'] = []
    session['uid'] = str(uuid.uuid4())
    return render_template('index.html')


@server.route('/show_progress', methods=['POST'])
def show_progress():
    """
    시작 화면에서 넘겨받은 인자를 통해 검사를 진행합니다.
    """
    api_url = request.form.get('api_url')
    check_list = request.form.getlist('category')

    session['use_subject'] = True if "subject" in check_list else False
    session['use_descriptive'] = True if "descriptive" in check_list else False

    # subject, descriptive don't need check_list but they will be use separately
    if "subject" in check_list:
        check_list.remove("subject")
    if "descriptive" in check_list:
        check_list.remove("descriptive")
    session['check_list'] = check_list
    check_str = "|".join(check_list)
    return render_template('progress.html', check_list=check_list, check_str=check_str)


@server.route('/check/<category>', methods=['GET'])
@param_check
def check(category):
    """
    category에 해당하는 검사를 진행 후 결과를 반환합니다.
    """
    result = controller.check(
        category, session['use_subject'], session['use_descriptive'])
    if result['status'] == "success":
        resultQ[session['uid']+category] = result['result']
    return {"status": result['status']}


@server.route('/fuzz_done', methods=['GET'])
@param_check
def fuzz_done():
    """
    fuzzing이 완료되었을 때 호출되는 함수입니다.
    """
    session['fuzzed'] = True
    return redirect(url_for('show_result'))


@server.route('/show_result', methods=['GET'])
@param_check
@fuzzed_check
def show_result():
    """
    결과를 보여주는 페이지
    """
    key = session['uid']
    check_list = session['check_list']
    full_result = {c: resultQ[key+c] for c in check_list}
    for c in check_list:
        del resultQ[key+c]
    result_data = controller.parse_result(
        session['check_list'], full_result, session['use_subject'], session['use_descriptive'])
    result = result_data['json']
    top_result = result_data['top']
    total_queryed = result_data['total_queryed']
    total_detected = result_data['total_detected']
    high_cnt = result_data['high_cnt']
    return render_template('charts.html',
                           result=result,
                           top_result=top_result,
                           total_queryed=total_queryed,
                           total_detected=total_detected,
                           high_level_count=high_cnt,
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


@server.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')


@server.route('/flag', methods=['GET'])
def flag():
    return render_template('charts.html')
    return {"flag": "This_SERVICE_is_NOT_CTF_Prob!!!!!!!!!!!"}


if __name__ == '__main__':
    server.run(host='0.0.0.0', debug=True)
