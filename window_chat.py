from tkinter import Toplevel
from tkinter.scrolledtext import ScrolledText
from tkinter import Text, Button, Frame, Label
from tkinter import LEFT, END, UNITS
from time import localtime, time, strftime



class WindowChat(Toplevel):  # 一个程序只有一个TK可以被继承
    def __init__(self):
        """
        这是聊天对话框
        """
        super(WindowChat, self).__init__()

        self.geometry(f'{800}x{500}')  # 初始大小

        self.resizable(False, False)  # 不能拉伸

        # 添加组件
        self.add_widget()

        # 测试代码
        # 发送按钮测试
        # self.on_send_button_click(lambda :print('test'))
        # 文本框和button按钮测试
        # self.on_send_button_click(lambda :print(self.get_input()))
        # 清空文本
        # self.on_send_button_click(lambda :print(self.clear_input()))
        # self.on_send_button_click(lambda :self.addend_message('这是','xx'))


    def add_widget(self):
        """
        添加组件
        :return:
        """
        # 聊天区域
        chat_text_area = ScrolledText(self, )  # 没有自己命名，在下面通过键值对命名
        chat_text_area['width'] = 110
        chat_text_area['height'] = 23
        chat_text_area.grid(row=0, column=0, columnspan=2)  # 占用2列
        chat_text_area.tag_config('green', foreground='#008b00')
        chat_text_area.tag_config('system', foreground='red')
        self.children['chat_text_area'] = chat_text_area  # 命名方式二

        # 为聊天增加的拓展
        add_area = Frame(self, name='add_area')
        add_area['width'] = 110
        add_area['height'] = 7

        function1 = Label(add_area, name='function1')
        function1['text'] = '表情'
        function1.pack(side=LEFT, padx=1, pady=1)

        add_area.grid(row=1, columnspan=2)

        # 输入区域
        chat_input_area = Text(self, name='chat_input_area')
        chat_input_area['width'] = 100
        chat_input_area['height'] = 6
        chat_input_area.grid(row=2, column=0, pady=10)

        # 发送按钮
        send_button = Button(self, name='send_button')
        send_button['text'] = '发  送'
        send_button['width'] = 7
        send_button['height'] = 4
        send_button.grid(row=2, column=1)

    def set_tittle(self, title):
        """
        设置headline
        """
        self.title(f'欢迎 {title} 加入聊天服务器')

    def on_send_button_click(self, command):
        """
        :param command: 需要执行函数
        :return:
        """
        self.children['send_button']['command'] = command

    def get_input(self):
        """
        获取输入框内容
        :return:
        """
        return self.children['chat_input_area'].get(0.0, END)

    def clear_input(self):
        """
        清空输入框内容
        :return:
        """
        self.children['chat_input_area'].delete(0.0, END)

    def addend_message(self, sender, massage):
        """
        添加聊天消息
        :param sender:
        :param massage:
        :return:
        """
        # 根据市区进行转换
        sendtime = strftime('%Y-%m-%d %H:%M:%S', localtime(time()))
        send_info = f'{sender}:{sendtime}\n'
        self.children['chat_text_area'].insert(END, send_info, 'green')
        self.children['chat_text_area'].insert(END, ' ' + massage + '\n')

        # 向下滚动进度条
        self.children['chat_text_area'].yview_scroll(3, UNITS)  # 屏幕滚动

    def on_window_closed(self, command):
        """
        关闭窗口处理函数,在初始化被框架调用
        :param command:
        :return:
        """
        self.protocol('WM_DELETE_WINDOW', command)




if __name__ == '__main__':
    WindowChat().mainloop()
