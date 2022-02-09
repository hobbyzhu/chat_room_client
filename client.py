from request_protocol import Request_Protocol
from window_chat import WindowChat
from window_login import Window_Login
from client_sock import ClientSocket
from threading import Thread
from config import *
from tkinter.messagebox import showinfo  # 提示对话框
import sys


class Client(object):
    """这是客户端核心类"""

    def __init__(self):
        """初始化客户端登录窗口"""
        self.window = Window_Login()
        #  重置按钮初始化
        self.window.on_reset_button_click(self.clear_input)
        # 登录按钮初始化
        self.window.on_login_Button_click(self.send_login_date)
        # 关闭窗口关闭整个进程
        self.window.on_window_close(self.exit)


        """初始化客户端聊天窗口"""
        self.window_chat = WindowChat()
        self.window_chat.withdraw()  # 隐藏窗口
        self.window_chat.on_send_button_click(self.send_chat_date)  # 点击发送
        self.window_chat.on_window_closed(self.exit)  # 关闭窗口关闭整个进程

        # 创建客户端连接套接字
        self.conn = ClientSocket()

        # 重构if判断调用类型，提高可用性
        self.response_handle_function = {}
        # 登录调用
        self.register(Response_Login_Result, self.response_login_handle)
        # 聊天调用，没有调用register封装
        self.register(Response_Chat, self.response_chat_handle)

        # 在线用户名称
        self.username = None

        # 程序正在运行的标记
        self.is_runing = True

    def register(self, request_id, handle_function):
        """
        消息类型和函数进行封装，我感觉没吊用  id和函数进行关联
        :param request_id: 消息类型
        :param handle_function: 执行函数对象
        :return: None
        """
        self.response_handle_function[request_id] = handle_function

    def send_login_date(self):
        """登录按钮"""

        # 获取到用户输入的
        username = self.window.get_username()
        password = self.window.get_password()

        # 生成登录的协议文本
        request_test = Request_Protocol.request_login_result(username, password)

        # 发送到服务器
        print('客户端发送的文本-->', request_test)
        self.conn.send_data(request_test)


    def send_chat_date(self):
        """
        获取聊天框内容，清空输入框，并将聊天内容发送到服务器
        :return:
        """
        massage = self.window_chat.get_input()

        self.window_chat.clear_input()  # 清空输入框

        # 拼接协议文本
        request_text = Request_Protocol.request_chart(self.username, massage)

        # 发送消息内容
        self.conn.send_data(request_text)

        # 把自己发送的消息发送到窗口
        self.window_chat.addend_message('我 ', massage)



    def clear_input(self):
        """清空窗口内容"""
        self.window.clear_name()
        self.window.clear_password()

    def satrt_run(self):
        """
        主线程用来发送消息，子线程用来接受消息
        1.连接服务器
        2.创建多线程并开启,来处理服务器消息
        3.开启窗口的事件循环
        """
        self.conn.connect()
        Thread(target=self.response_handle).start()
        self.window.mainloop()

    def response_handle(self):
        """
        不断接受服务器新消息
        1.获取服务器消息
        2.判读消息内容并处理
        """
        while self.is_runing:
            recv_date = self.conn.recv_data()
            print('服务器返回的消息--》', recv_date)

            response_date = self.parse_response_date(recv_date)  # 调用解析函数

            # 根据key和方法的对应关系 选择执行函数
            handle_function = self.response_handle_function[response_date['response_id']]

            if handle_function:  # 当存在就执行
                handle_function(response_date)

    @staticmethod
    def parse_response_date(recv_date):
        """
        解析数据类型，静态方法
        1. 1001|成功/失败|昵称|账号
        2. 1002|发送者昵称|消息内容
        :param recv_date:服务器返回的数据
        :return:字典
        """
        response_date_list = recv_date.split(Delimiter)
        response_date = dict()
        response_date['response_id'] = response_date_list[0]

        print('test------------->', response_date['response_id'])

        if response_date['response_id'] == Response_Login_Result:  # 登录响应
            response_date['result'] = response_date_list[1]
            response_date['nickname'] = response_date_list[2]
            response_date['username'] = response_date_list[3]
        elif response_date['response_id'] == Response_Chat:  # 聊天响应
            response_date['nickname'] = response_date_list[1]
            response_date['massage'] = response_date_list[2]
        return response_date

    def response_login_handle(self, response_date):
        """
        登录处理分支
        :return:
        """
        print(f"开始登录")
        result = response_date['result']
        if result == '0':
            showinfo('提示信息', '登录失败')  # tk内置模块 标题和提示内容
            print('login fail')
            return

        showinfo('提示消息', '登录成功')
        nickname = response_date['nickname']
        self.username = response_date['username']  # 当前在线用户名称

        # 设置标题，刷新页面，显示聊天窗口
        self.window_chat.set_tittle(nickname)
        self.window_chat.update()
        self.window_chat.deiconify()

        # 隐藏登录窗口
        self.window.withdraw()

    def response_chat_handle(self, response_date):
        """
        聊天处理分支
        :return:
        """
        print('聊天处理')
        sender = response_date['nickname']
        massage = response_date['massage']
        if __name__ == '__main__':
            self.window_chat.addend_message(sender, massage)

    def exit(self):
        """退出程序"""
        self.is_runing = False  # 接受数据关闭，停止子线程
        self.conn.close()  # 关闭套接字
        sys.exit(0)  # 退出程序


if __name__ == '__main__':
    client = Client()
    client.satrt_run()
