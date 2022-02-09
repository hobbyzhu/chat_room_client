import socket
from config import *


class ClientSocket(socket.socket):
    """
    直接继承，代码会清晰
    客户端的套接子自定义处理
    """

    def __init__(self):
        # 设置为TCP套接字
        super(ClientSocket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """
        自动连接服务器
        """
        super(ClientSocket, self).connect((SERVER_IP, SERVER_PORT))

    def recv_data(self):
        """接受字节数据，并自动转为字符串"""
        return self.recv(512).decode('utf-8')

    def send_data(self, massage):
        """将字符串，转换为字节数据发送"""
        return self.send(massage.encode('utf-8'))
