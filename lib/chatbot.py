"""
API 서버에 메시지를 전달하여 응답을 받아오는 역할을 하는 클래스
This class is used to send message to API server and receive response
"""
import requests as req


class ChatBot:
    def __init__(self, API_URL):
        self.API_URL = API_URL

    def get_conf(self):
        pass
        #     with req.Session() as s:
        # try:
        #     r = s.get(api_url+"/conf")
        #     if r.text == "":
        #         raise APIConfGetError()
            
        # except req.exceptions.Timeout:
        #     return {"status":"error", "msg":"Timeout"}
        # except req.exceptions.ConnectionError:
        #     return {"status":"error", "msg":"Connection Error"}
        # except req.exceptions.RequestException as e:
        #     return {"status":"error", "msg":e.response.text}
        # except APIConfGetError:
        #     return {"status":"error", "msg":APIConfGetError}
        # except:
        #     return {"status":"error", "msg":"Unknown Error"}
    def talk(self, msg):
        """
        Input: msg=str
        Output: msg=str
        """
        data = {'msg': msg}
        r = req.post(self.API_URL+"/talk", data=data)
        return r.text