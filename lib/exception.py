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