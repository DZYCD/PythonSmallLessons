#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Time    : 2025/4/9 上午9:45
# @Author  : 单子叶蚕豆_DzyCd
# @File    : Permission.py
# @IDE     : PyCharm
permission_list = ['用户', '业务员', '管理员', '出库员', '入库员']
user_list = []


class USER:
    def __init__(self):
        self.permit = 0
        self.pwd = ''
        self.name = ''
        self.login = False
        self.lock = False
        self.try_time = 3
        self._initialize_default_user()

    def _initialize_default_user(self):
        self.permit = 2
        self.pwd = '123'
        self.name = 'DzyCd'
        self.login = False
        self.lock = False
        user_list.append(self)

    def _create_new_user(self):
        s = USER()
        if self.login == True and (self.permit == 2 or self.permit == 1):
            print('新建用户')
            s.name = input('用户名>>>')
            while True:
                try:
                    print("权限列表： ['用户', '业务员', '管理员', '出库员', '入库员']")
                    s.permit = int(input('权限等级>>>'))
                    if s.permit == 2 and self.permit == 1:
                        print("越权操作，业务员不可增设管理员")
                        print(int('DzyCd'))
                    break
                except:
                    print('重试')
            s.pwd = '123'
            print('初始密码 123，请登录后修改密码')
            user_list.append(s)
            print('创建完成')

    def create_new_user(self, username, password, permit):
        s = USER()
        s.name = username
        s.permit = permit
        s.pwd = password
        user_list.append(s)

    def change_code(self):
        if self.login == True:
            while True:
                code = input('请输入新密码')
                confirm = input('请确认新密码')
                if code == confirm:
                    self.pwd = code
                    print('密码设置成功！')
                    return
                else:
                    print('前后密码不相同，请重新输入！')

    def enter_code(self):
        if self.lock:
            print('账户锁定中，禁止登录，请联系管理员')
            return

        if self.login:
            print('禁止重复登录！')
            return

        for i in range(3):
            pwd = input(f'输入用户{self.name}密码：')
            if pwd == self.pwd:
                self.login = True
                print('登陆成功!')
                return
            else:
                print(f'登录失败...还有({2-i})次')

        print('尝试机会耗尽，账户已被锁定，请联系管理员')
        self.lock = True

    def recover_user(self):
        if self.login and self.permit == 2:
            print('当前锁定账户：')
            for i in user_list:
                if i.lock == True:
                    print(f'名称{i.name}  权限等级{permission_list[i.permission]}  密码{i.pwd}')

            name = input('恢复用户名')
            for i in user_list:
                if i.name == name:
                    i.lock = False
                    i.pwd = '123'
                    print('账户已恢复，密码恢复为123')

    def delete_user(self):
        if self.login and self.permit == 2:
            print('当前所有用户：')
            for i in user_list:
                print(f'名称{i.name}  权限等级{permission_list[i.permission]}  密码{i.pwd}')
        name = input('删除用户名')
        for i in user_list:
            if i.name == name:
                del i
                print('账户已删除')

    def show_user(self):
        if self.login and self.permit == 2:
            print('当前所有用户：')
            for i in user_list:
                print(f'名称{i.name}  权限等级{permission_list[i.permission]}  密码{i.pwd}')
