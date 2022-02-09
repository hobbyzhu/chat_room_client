from config import *


class Request_Protocol(object):

    @staticmethod
    def request_login_result(username, password):
        """
        登录客户端字符串拼接
        0001|username|password  类型|账号|密码
        :return: 完整的登录数据
        """
        return Delimiter.join([Request_Login, username, password])

    @staticmethod
    def request_chart(username, massage):
        """
        0002|username|massage 类型|账号|聊天内容
        :return: 完整的聊天数据
        """
        return Delimiter.join([Request_Chat, username, massage])
