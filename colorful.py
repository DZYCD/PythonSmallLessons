#!/usr/bin/python3
# _*_ coding: utf-8 _*_
#
# @Time    : 2025/4/10 下午8:08
# @Author  : 单子叶蚕豆_DzyCd
# @File    : main.py
# @IDE     : PyCharm
from tkinter import *
from tkinter import messagebox, ttk
import webbrowser

import Permission
from operations import *
import datetime


class WarehouseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ISOM 货物仓储平台\n 软工231 李梓鸣 2330110474 \n UI界面版")
        self.root.geometry("800x600")
        self.root.configure(bg='#e6e6fa')
        self.bg_color = '#e6e6fa'
        self.fg_color = '#4b0082'
        self.button_bg = '#9370db'
        self.button_fg = 'white'
        self.highlight_color = '#d8bfd8'

        self.user = Permission.USER()
        self.manager = WarehouseManager()

        self.create_login_screen()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_login_screen(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="ISOM 货物仓储平台\n 软工231 李梓鸣 2330110474 \n UI界面版",
              font=("Arial", 20), fg=self.fg_color, bg=self.bg_color).pack(pady=20)

        frame = Frame(self.root, bg=self.bg_color)
        frame.pack(pady=20)

        Label(frame, text="用户名:", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5)
        self.username_entry = Entry(frame)
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(frame, text="密码:", fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0, padx=5, pady=5)
        self.password_entry = Entry(frame, show="*")
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        Button(self.root, text="登录", command=self.login, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Label(self.root, text="如需注册新账户请联系管理员", fg="gray", bg=self.bg_color).pack()
        Label(self.root, text="管理员账号DzyCd, 密码123；任何账号在三次密码输入错误后锁定，可以被管理员恢复", fg="green", bg=self.bg_color).pack()
        Label(self.root, text="简介： 具有四种权限设置，管理员可以注册新用户；利用tkinter展示更清晰；", fg="purple", bg=self.bg_color).pack()
        Label(self.root, text="在原有基础之上增加改密码、改用户、登出、锁定恢复账号、增设仓库等功能；", fg="purple", bg=self.bg_color).pack()
        Label(self.root, text="物品入库需要符合仓库种类要求；另增设万用库（*）可存放一切物品；", fg="purple",bg=self.bg_color).pack()
        Label(self.root, text="ISOM独特的淡紫色格调；库存分片存储，存储性能更优化，使用最佳匹配算法；", fg="purple", bg=self.bg_color).pack()
        Button(root, text="看看这个DzyCd是什么玩意", command=self.open_url, width=20).pack(pady=50)

    def open_url(self):
        url = "https://github.com/DZYCD"  # 替换为你想要跳转的URL
        webbrowser.open_new(url)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user_found = False
        for user in Permission.user_list:
            if user.name == username:
                if user.lock:
                    messagebox.showerror("错误", "账户被锁定，请联系管理员恢复账号")
                    return
                if user.pwd == password:
                    user.try_time = 3
                    self.user = user
                    user.login = True
                    self.create_main_menu()
                    return
                else:
                    user.try_time -= 1
                    if user.try_time == 0:
                        user.lock = True
                        messagebox.showerror("错误", "密码重试次数太多，账号已锁定")
                    else:
                        messagebox.showerror("错误", "密码错误")
                    return

        if not user_found:
            messagebox.showerror("错误", "未找到该用户")

    def create_main_menu(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        if self.user.login == False or self.user.lock:
            messagebox.showerror("错误", "请先登录")
            self.user.login = False
            self.create_login_screen()
            return

        header = Frame(self.root, bg=self.bg_color)
        header.pack(fill=X, padx=10, pady=10)

        Label(header, text=f"用户: {self.user.name} | {Permission.permission_list[self.user.permit]}",
              font=("Arial", 12), fg=self.fg_color, bg=self.bg_color).pack(side=LEFT)

        Button(header, text="退出", command=self.logout, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(side=RIGHT)

        menu_frame = Frame(self.root, bg=self.bg_color)
        menu_frame.pack(pady=20)

        buttons = [
            ("新增仓储货物信息", self.create_goods_ui),
            ("货物入库", self.stock_in_ui),
            ("货物出库", self.stock_out_ui),
            ("修改货物信息", self.update_goods_ui),
            ("查询库存", self.query_goods_ui),
            ("查询出入库记录", self.query_logs_ui),
            ("用户管理", self.user_management_ui),
            ("创建新库", self.create_warehouse_ui)
        ]

        for i, (text, command) in enumerate(buttons):
            if i == 1 and self.user.permit == 3:
                continue
            if i == 2 and self.user.permit == 4:
                continue
            if i in [0, 1, 2, 3] and self.user.permit < 2:
                continue
            if i == 5 and self.user.permit < 1:
                continue
            if i == 7 and self.user.permit != 2:
                continue
            Button(menu_frame, text=text, width=25, command=command,
                   bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)

    def exit(self):
        self.user.login = False
        self.login()

    def logout(self):
        self.user.login = False
        self.create_login_screen()

    def create_goods_ui(self):
        if self.user.permit < 2:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="新增仓储货物信息", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        form_frame = Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=10)

        labels = ["名称:", "种类:", "长度:", "宽度:", "生产日期:", "过期日期:"]
        entries = []

        for i, label in enumerate(labels):
            Label(form_frame, text=label, fg=self.fg_color, bg=self.bg_color).grid(row=i, column=0, padx=5, pady=5,
                                                                                   sticky=E)
            entry = Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)

        entries[4].insert(0, datetime.date.today().strftime("%Y-%m-%d"))
        entries[5].insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        def submit():
            try:
                name = entries[0].get()
                category = entries[1].get()
                length = int(entries[2].get())
                width = int(entries[3].get())
                production_date = datetime.datetime.strptime(entries[4].get(), "%Y-%m-%d").date()
                expiry_date = datetime.datetime.strptime(entries[5].get(), "%Y-%m-%d").date()

                self.manager.create_goods(
                    id=len(self.manager.goods),
                    name=name,
                    category=category,
                    length=length,
                    width=width,
                    production_date=production_date,
                    expiry_date=expiry_date
                )
                messagebox.showinfo("成功", "货物信息已添加")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("错误", f"输入有误: {str(e)}")

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def stock_in_ui(self):
        if self.user.permit not in [2, 4]:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="货物入库", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        available_goods = [g for g in self.manager.goods if g.warehouse_id == 0]

        if not available_goods:
            Label(self.root, text="没有可入库的货物", fg=self.fg_color, bg=self.bg_color).pack()
            Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
                   activebackground=self.highlight_color).pack()
            return

        goods_frame = Frame(self.root, bg=self.bg_color)
        goods_frame.pack(pady=10)

        Label(goods_frame, text="选择货物:", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0)

        self.goods_var = StringVar()
        goods_options = [f"{g.id}, {g.name}, 宽{g.width}, 长{g.length}, 种类{g.category}" for g in available_goods]
        goods_dropdown = ttk.Combobox(goods_frame, textvariable=self.goods_var, values=goods_options, state="readonly")
        goods_dropdown.grid(row=0, column=1)
        goods_dropdown.current(0)

        Label(goods_frame, text="选择仓库:", fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0)

        self.warehouse_var = StringVar()
        warehouse_options = [f"{w.id}, {w.name}, 宽{w.width}, 长{w.length}" for w in self.manager.warehouses]
        warehouse_dropdown = ttk.Combobox(goods_frame, textvariable=self.warehouse_var, values=warehouse_options,
                                          state="readonly")
        warehouse_dropdown.grid(row=1, column=1)
        if warehouse_options:
            warehouse_dropdown.current(0)

        def submit():
            try:
                goods_id = int(self.goods_var.get().split(",")[0])
                warehouse_id = int(self.warehouse_var.get().split(",")[0])

                if not self.manager.stock_in(goods_id, warehouse_id):  # 这里可以控制防止线程池重复录入
                    messagebox.showerror("错误", "仓库没有足够的空间存放该货物")
                    self.create_main_menu()
                    return
                messagebox.showinfo("成功", "货物已入库")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def stock_out_ui(self):
        if self.user.permit not in [2, 3]:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="货物出库", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        available_goods = [g for g in self.manager.goods if g.warehouse_id != 0]

        if not available_goods:
            Label(self.root, text="没有可出库的货物", fg=self.fg_color, bg=self.bg_color).pack()
            Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
                   activebackground=self.highlight_color).pack()
            return

        goods_frame = Frame(self.root, bg=self.bg_color)
        goods_frame.pack(pady=10)

        Label(goods_frame, text="选择货物:", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0)

        self.goods_var_out = StringVar()
        goods_options = [f"{g.id}, {g.name}, 宽{g.width}, 长{g.length}, 种类{g.category}" for g in available_goods]
        goods_dropdown = ttk.Combobox(goods_frame, textvariable=self.goods_var_out, values=goods_options,
                                      state="readonly")
        goods_dropdown.grid(row=0, column=1)
        goods_dropdown.current(0)

        def submit():
            try:  # 这里可以控制防止线程池重复出库
                goods_id = int(self.goods_var_out.get().split(",")[0])

                if self.manager.stock_out(goods_id):
                    messagebox.showinfo("成功", "货物已出库")
                else:
                    messagebox.showerror("错误", f"禁止重复出库")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def update_goods_ui(self):
        if self.user.permit < 2:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="修改货物信息", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        goods_frame = Frame(self.root, bg=self.bg_color)
        goods_frame.pack(pady=10)

        Label(goods_frame, text="选择货物:", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0)

        self.goods_var_update = StringVar()
        goods_options = [f"{g.id}, {g.name}, 宽{g.width}, 长{g.length}, 种类{g.category}" for g in self.manager.goods]
        goods_dropdown = ttk.Combobox(goods_frame, textvariable=self.goods_var_update, values=goods_options,
                                      state="readonly")
        goods_dropdown.grid(row=0, column=1)
        if goods_options:
            goods_dropdown.current(0)

        form_frame = Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=10)

        labels = ["名称:", "种类:", "长度:", "宽度:", "过期日期:"]
        self.update_entries = []

        for i, label in enumerate(labels):
            Label(form_frame, text=label, fg=self.fg_color, bg=self.bg_color).grid(row=i, column=0, padx=5, pady=5,
                                                                                   sticky=E)
            entry = Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.update_entries.append(entry)

        self.update_entries[4].insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        def load_goods_info(event=None):
            try:
                goods_id = int(self.goods_var_update.get().split(",")[0])
                goods = next(g for g in self.manager.goods if g.id == goods_id)

                for entry in self.update_entries:
                    entry.delete(0, END)

                self.update_entries[0].insert(0, goods.name)
                self.update_entries[1].insert(0, goods.category)
                self.update_entries[2].insert(0, str(goods.length))
                self.update_entries[3].insert(0, str(goods.width))
                self.update_entries[4].insert(0, goods.expiry_date.strftime("%Y-%m-%d"))
            except:
                pass

        goods_dropdown.bind("<<ComboboxSelected>>", load_goods_info)
        if goods_options:
            load_goods_info()

        def submit():
            try:
                goods_id = int(self.goods_var_update.get().split(",")[0])
                name = self.update_entries[0].get()
                category = self.update_entries[1].get()
                length = int(self.update_entries[2].get())
                width = int(self.update_entries[3].get())
                expiry_date = datetime.datetime.strptime(self.update_entries[4].get(), "%Y-%m-%d").date()

                self.manager.update_goods_info(
                    goods_id,
                    name=name,
                    category=category,
                    length=length,
                    width=width,
                    expiry_date=expiry_date
                )
                messagebox.showinfo("成功", "货物信息已更新")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("错误", f"输入有误: {str(e)}")

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def query_goods_ui(self):
        if self.user.permit < 1:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="查询库存", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        text_frame = Frame(self.root)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_widget = Text(text_frame, wrap=WORD, yscrollcommand=scrollbar.set, bg='white', fg='black')
        text_widget.pack(fill=BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        goods_info = self.manager.query_goods()
        text_widget.insert(END, goods_info)
        text_widget.config(state=DISABLED)

        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)

    def query_logs_ui(self):
        if self.user.permit < 1:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="查询出入库记录", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        text_frame = Frame(self.root)
        text_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=RIGHT, fill=Y)

        text_widget = Text(text_frame, wrap=WORD, yscrollcommand=scrollbar.set, bg='white', fg='black')
        text_widget.pack(fill=BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        logs_info = self.manager.query_operation_logs()
        text_widget.insert(END, logs_info)
        text_widget.config(state=DISABLED)

        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)

    def user_management_ui(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="用户管理", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        options_frame = Frame(self.root, bg=self.bg_color)
        options_frame.pack(pady=10)

        Button(options_frame, text="修改密码", command=self.change_password_ui,
               bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)

        if self.user.permit == 2:
            Button(options_frame, text="注册新用户", command=self.create_user_ui,
                   bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)
            Button(options_frame, text="账号锁定/恢复", command=self.lock_user_ui,
                   bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)

        Button(options_frame, text="登出", command=self.logout,
               bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)
        Button(options_frame, text="返回", command=self.create_main_menu,
               bg=self.button_bg, fg=self.button_fg, activebackground=self.highlight_color).pack(pady=5)

    def lock_user_ui(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)
        Label(self.root, text="选择用户", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=20)

        goods_frame = Frame(self.root, bg=self.bg_color)
        goods_frame.pack(pady=20)
        self.goods_var_out = StringVar()
        goods_options = [f"{g.name}, {Permission.permission_list[g.permit]}, 密码{g.pwd}, 锁定状态{str(g.lock)}" for g in Permission.user_list]
        goods_dropdown = ttk.Combobox(goods_frame, textvariable=self.goods_var_out, values=goods_options,
                                      state="readonly")
        goods_dropdown.grid(row=0, column=1)
        goods_dropdown.current(0)

        def submit_lock():
            try:
                name = self.goods_var_out.get().split(',')[0]
                for i in Permission.user_list:
                    if i.name == name:
                        i.lock = True
                        messagebox.showinfo("成功", f"锁定成功")
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

        def submit_recover():
            try:
                name = self.goods_var_out.get().split(',')[0]
                for i in Permission.user_list:
                    if i.name == name:
                        i.lock = False
                        messagebox.showinfo("成功", f"恢复成功")
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

        Button(self.root, text="锁定", command=submit_lock, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="恢复", command=submit_recover, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.create_main_menu, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()


    def change_password_ui(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="修改密码", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        form_frame = Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=10)

        Label(form_frame, text="当前密码:", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, padx=5, pady=5,
                                                                                     sticky=E)
        self.current_pass_entry = Entry(form_frame, show="*")
        self.current_pass_entry.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="新密码:", fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0, padx=5, pady=5,
                                                                                   sticky=E)
        self.new_pass_entry = Entry(form_frame, show="*")
        self.new_pass_entry.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="确认新密码:", fg=self.fg_color, bg=self.bg_color).grid(row=2, column=0, padx=5, pady=5,
                                                                                       sticky=E)
        self.confirm_pass_entry = Entry(form_frame, show="*")
        self.confirm_pass_entry.grid(row=2, column=1, padx=5, pady=5)

        def submit():
            current = self.current_pass_entry.get()
            new = self.new_pass_entry.get()
            confirm = self.confirm_pass_entry.get()

            if current != self.user.pwd:
                messagebox.showerror("错误", "当前密码不正确")
                return

            if new != confirm:
                messagebox.showerror("错误", "新密码不匹配")
                return

            self.user.pwd = new
            messagebox.showinfo("成功", "密码已修改")
            self.create_main_menu()

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.user_management_ui, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def create_warehouse_ui(self):
        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="创建新库", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        form_frame = Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=10)

        Label(form_frame, text="新库名称", fg=self.fg_color, bg=self.bg_color).grid(row=0, column=0, padx=5,
                                                                                pady=5,
                                                                                sticky=E)
        self.current_name = Entry(form_frame)
        self.current_name.grid(row=0, column=1, padx=5, pady=5)

        Label(form_frame, text="长度", fg=self.fg_color, bg=self.bg_color).grid(row=1, column=0, padx=5,
                                                                                pady=5,
                                                                                sticky=E)
        self.current_length = Entry(form_frame)
        self.current_length.grid(row=1, column=1, padx=5, pady=5)

        Label(form_frame, text="宽度", fg=self.fg_color, bg=self.bg_color).grid(row=2, column=0, padx=5, pady=5,
                                                                                sticky=E)
        self.current_width = Entry(form_frame)
        self.current_width.grid(row=2, column=1, padx=5, pady=5)

        Label(form_frame, text="种类（*代表杂物库）", fg=self.fg_color, bg=self.bg_color).grid(row=3, column=0, padx=5, pady=5,
                                                                                sticky=E)
        self.current_category = Entry(form_frame)
        self.current_category.grid(row=3, column=1, padx=5, pady=5)

        Label(form_frame, text="分片大小", fg=self.fg_color, bg=self.bg_color).grid(row=4, column=0, padx=5,
                                                                                    pady=5,
                                                                                    sticky=E)
        self.current_size = Entry(form_frame)
        self.current_size.grid(row=4, column=1, padx=5, pady=5)

        def submit():
            try:
                self.manager.create_warehouse(self.current_name.get(), int(self.current_length.get()), int(self.current_width.get()), self.current_category.get(), int(self.current_size.get()))
                messagebox.showinfo("成功", "新库已完成创建")
                self.create_main_menu()
            except:
                messagebox.showerror("错误", "长、宽、分片大小必须为整数")
                return

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.user_management_ui, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()

    def create_user_ui(self):
        if self.user.permit != 2:
            messagebox.showerror("错误", "无权限")
            return

        self.clear_frame()
        self.root.configure(bg=self.bg_color)

        Label(self.root, text="注册新用户", font=("Arial", 16),
              fg=self.fg_color, bg=self.bg_color).pack(pady=10)

        form_frame = Frame(self.root, bg=self.bg_color)
        form_frame.pack(pady=10)

        labels = ["用户名:", "密码:"]
        entries = []

        var = IntVar()
        var.set(1)

        label = Label(self.root, text="权限级别 (1-4):", fg=self.fg_color, bg=self.bg_color)
        label.pack(pady=10)
        msg = ["0.游客", "1.业务员", "2.管理员", "3.出库员", "4.入库员"]
        for i in range(1, 5):
            Radiobutton(self.root, text=msg[i], variable=var, value=i, padx=5, pady=5,
                        fg=self.fg_color, bg=self.bg_color, selectcolor=self.highlight_color).pack(anchor="center")

        for i, label in enumerate(labels):
            Label(form_frame, text=label, fg=self.fg_color, bg=self.bg_color).grid(row=i, column=0, padx=5, pady=5,
                                                                                   sticky=E)
            entry = Entry(form_frame)
            entry.grid(row=i, column=1, padx=5, pady=5)
            entries.append(entry)
        entries.append(var)

        def submit():
            try:
                username = entries[0].get()
                password = entries[1].get()
                permit = int(entries[2].get())

                if permit < 1 or permit > 4:
                    messagebox.showerror("错误", "权限级别必须在1-4之间")
                    return

                self.user.create_new_user(username, password, permit)
                messagebox.showinfo("成功", "用户已创建")
                self.create_main_menu()
            except Exception as e:
                messagebox.showerror("错误", f"创建用户失败: {str(e)}")

        Button(self.root, text="提交", command=submit, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack(pady=10)
        Button(self.root, text="返回", command=self.user_management_ui, bg=self.button_bg, fg=self.button_fg,
               activebackground=self.highlight_color).pack()


if __name__ == "__main__":
    root = Tk()
    app = WarehouseApp(root)
    root.mainloop()