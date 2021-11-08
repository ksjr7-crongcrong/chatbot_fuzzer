"""
API 서버에 메시지를 전달하여 응답을 받아오는 역할을 하는 클래스
This class is used to send message to API server and receive response
"""
import requests as req


class ChatBot:
    def __init__(self, API_URL):
        self.API_URL = API_URL
        self.get_conf()

    def get_conf(self):
        """
        conf endpoint로 부터 interval 값을 받아옴
        """
        r = req.get(self.API_URL+"/conf")
        self.interval = r.json()['interval']

    def talk(self, msg):
        """
        Input: msg=str
        Output: msg=str
        talk endpoint를 통해 chatbot에게 메시지를 보내고 답변을 받아옴
        """
        data = {'msg': msg}
        r = req.post(self.API_URL+"/talk", data=data)
        msg = r.json()['msg']
        return msg