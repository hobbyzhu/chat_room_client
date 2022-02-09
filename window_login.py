from tkinter import Tk
from tkinter import Label, Entry, Frame, Button, LEFT, END


# 直接继承
class Window_Login(Tk):
    """
    登录窗口
    """

    def __init__(self):
        """
        兼容性
        """
        super(Window_Login, self).__init__()
        # super().__init__()

        # 设置窗口属性
        self.window_init()

        # 填充控件
        self.add_widgets()

        # 控件测试
        # self.on_login_Button_click(lambda: print(self.get_password()))
        # self.on_reset_button_click(lambda: self.clear_password())


    def window_init(self):
        """
        窗口初始化属性
        :return:
        """
        # 设置窗口的标题
        self.title('登录窗口')

        # 设置窗口不能拉伸
        self.resizable(False, False)

        # 窗口大小
        window_width = 255
        window_high = 90
        # 获取屏幕大小
        screen_width = self.winfo_screenwidth()
        screen_high = self.winfo_screenheight()

        # 换算窗口位置
        pos_x = screen_width // 2 - window_width // 2
        pos_y = screen_high // 2 - window_high // 2

        # 设置窗口大小和位置
        self.geometry(f'{window_width}x{window_high}+{pos_x}+{pos_y}')  # 字符型(高x宽+x+y)

    def add_widgets(self):
        """
        添加控件到窗口
        :return:
        """
        # 用户名 第一行
        username_label = Label(self)
        username_label['text'] = '用户名:'
        username_label.grid(row=0, column=0, padx=10, pady=5)  # (行 ，列，上间距padding，下）

        username_entry = Entry(self, name='username_entry')
        username_entry['width'] = 17
        username_entry.grid(row=0, column=1, )

        # 密码区 第二行
        password_label = Label(self)
        password_label['text'] = '密  码:'
        password_label.grid(row=1, column=0)

        password_entry = Entry(self, name='password_entry')
        password_entry['width'] = 17
        password_entry['show'] = '*'  # 设置密码掩码
        password_entry.grid(row=1, column=1, )

        # 创建Frame容器 第三行
        button_frame = Frame(self, name='button_frame')
        # 重置
        reset_button = Button(button_frame, name='reset_button')  # 注意父容器已经变成了Frame了，将button加入到容器中
        reset_button.pack(side=LEFT, padx=20, pady=1)  # 左对齐
        reset_button['text'] = '重置'
        # 登录
        login_button = Button(button_frame, name='login_button')  # 注意父容器已经变成了Frame了，将button加入到容器中
        login_button.pack(side=LEFT)
        login_button['text'] = '登录'

        # 触发button，已经封装在外部
        # login_button['command'] = lambda: print('xx')

        # frame容器布局
        button_frame.grid(row=2, columnspan=2, pady=5)  # 第三行，columnspan表示本行全占了


    def get_username(self):
        """
        获取用户名
        :return: username
        """
        return self.children['username_entry'].get()

    def get_password(self):
        """
        获取密码
        :return: password
        """
        return self.children['password_entry'].get()

    def clear_name(self):
        """
        删除登录文本框中的内容
        :return:None
        """
        self.children['username_entry'].delete(0, END)

    def clear_password(self):
        """
        删除密码文本框中的内容
        :return:None
        """
        self.children['password_entry'].delete(0, END)


    def on_login_Button_click(self, command):
        """
        登录按钮的响应注册
        :param command: 需要运行的函数
        :return: None
        """
        login_button = self.children['button_frame'].children['login_button']  # 子窗口的子窗口对象
        login_button['command'] = command   # 将函数绑定到login_button按钮,点击就触发

    def on_reset_button_click(self, command):
        """
        重置按钮的响应
        :param command:需要运行的函数
        :return:
        """
        reset_button = self.children['button_frame'].children['reset_button']
        reset_button['command'] = command

    def on_window_close(self, command):
        """
        关闭窗口响应注册，关闭窗口处理函数,在初始化被框架调用
        """
        # 设置关闭创建事件
        self.protocol('WM_DELETE_WINDOW', command)



if __name__ == '__main__':
    window = Window_Login()
    window.mainloop()
