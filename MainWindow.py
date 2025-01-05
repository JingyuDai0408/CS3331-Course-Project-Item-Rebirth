from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, 
    QComboBox, QFormLayout, QLabel, QTabWidget, QDialog, QMessageBox, QStackedWidget, QTabWidget
)

from Item import Item
from ItemManager import ItemManager
from User import OrdinaryUser, AdministratorUser
from UserManager import UserManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.item_manager = ItemManager()
        self.user_manager = UserManager()
        self.setWindowTitle("物品复活系统")
        self.setGeometry(100, 100, 1000, 800)

        # 创建一个 QStackedWidget 实现顺序模式
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 添加选项卡
        self.registration_tab = self.create_registration_tab()  # 用户注册
        self.stacked_widget.addWidget(self.registration_tab)

        self.login_tab = self.create_login_tab()  # 用户登录
        self.stacked_widget.addWidget(self.login_tab)

        self.main_tab = self.create_main_tab()  # 主界面
        self.stacked_widget.addWidget(self.main_tab)

        # 初始显示用户注册界面
        self.stacked_widget.setCurrentWidget(self.registration_tab)

    # 创建用户注册界面
    def create_registration_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.address_input = QLineEdit()
        self.phone_input = QLineEdit()
        self.email_input = QLineEdit()

        self.register_button = QPushButton("注册用户")
        self.register_button.clicked.connect(self.register_user)
        
        self.go_to_login_button = QPushButton("去登录")
        self.go_to_login_button.clicked.connect(self.go_to_login)
        
        # 注册成为管理员按钮
        self.register_as_admin_button = QPushButton("注册成为管理员")
        self.register_as_admin_button.clicked.connect(self.register_as_admin)

        layout.addWidget(QLabel("用户名"))
        layout.addWidget(self.username_input)
        layout.addWidget(QLabel("密码"))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel("地址"))
        layout.addWidget(self.address_input)
        layout.addWidget(QLabel("电话"))
        layout.addWidget(self.phone_input)
        layout.addWidget(QLabel("邮箱"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.register_button)
        layout.addWidget(self.register_as_admin_button)
        layout.addWidget(self.go_to_login_button)

        tab.setLayout(layout)
        return tab

    # 创建用户登录界面
    def create_login_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.login_username_input = QLineEdit()
        self.login_password_input = QLineEdit()

        self.login_button = QPushButton("登录")
        self.login_button.clicked.connect(self.login_user)
        
        self.go_to_register_button = QPushButton("去注册")
        self.go_to_register_button.clicked.connect(self.go_to_register)

        layout.addWidget(QLabel("用户名"))
        layout.addWidget(self.login_username_input)
        layout.addWidget(QLabel("密码"))
        layout.addWidget(self.login_password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.go_to_register_button)

        tab.setLayout(layout)
        return tab

    # 创建主界面
    def create_main_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.tabs = QTabWidget()
        self.item_management_tab = self.create_item_management_tab()
        self.account_management_tab = self.create_account_management_tab()
        self.tabs.addTab(self.item_management_tab, "物品管理")
        self.tabs.addTab(self.account_management_tab, "账户管理")

        layout.addWidget(self.tabs)

        tab.setLayout(layout)
        return tab

    # 创建主界面中的物品管理界面选项卡
    def create_item_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.item_name_input = QLineEdit()
        self.item_description_input = QLineEdit()
        self.item_address_input = QLineEdit()
        self.item_phone_input = QLineEdit()
        self.item_email_input = QLineEdit()

        self.item_type_combo = QComboBox()
        self.item_type_combo.addItems(self.item_manager.item_types)
        self.item_type_combo.currentIndexChanged.connect(self.update_extra_fields)
        
        # 初始选择为“食品”
        self.item_type_combo.setCurrentText("食品")
    
        self.extra_layout = QFormLayout()
        
        # 初始显示食品类型的所有属性
        attributes = self.item_manager.get_item_type_attributes("食品")

        for attr in attributes:
            input_field = QLineEdit()
            self.extra_layout.addRow(attr, input_field)

        # 添加物品按钮
        self.add_item_button = QPushButton("添加物品")
        self.add_item_button.clicked.connect(self.add_item)
        
        # 删除物品按钮
        self.delete_item_button = QPushButton("删除物品")
        self.delete_item_button.clicked.connect(self.delete_item)

        # 查询物品按钮
        self.search_item_button = QPushButton("查询物品")
        self.search_item_button.clicked.connect(self.search_item_dialog)

        # 展示全部物品按钮
        self.show_all_items_button = QPushButton("展示全部物品")
        self.show_all_items_button.clicked.connect(self.show_all_items)
        
        # 物品列表
        self.item_list_table = QTableWidget()
        self.item_list_table.setColumnCount(8)
        self.item_list_table.setHorizontalHeaderLabels(["物品名称", "描述", "地址", "联系人手机", "邮箱", "物品类型", "发布者姓名", "删除"])

        layout.addWidget(QLabel("物品名称"))
        layout.addWidget(self.item_name_input)
        layout.addWidget(QLabel("物品描述"))
        layout.addWidget(self.item_description_input)
        layout.addWidget(QLabel("物品地址"))
        layout.addWidget(self.item_address_input)
        layout.addWidget(QLabel("联系人电话"))
        layout.addWidget(self.item_phone_input)
        layout.addWidget(QLabel("联系人邮箱"))
        layout.addWidget(self.item_email_input)
        layout.addWidget(QLabel("物品类型"))
        layout.addWidget(self.item_type_combo)

        layout.addLayout(self.extra_layout)
        layout.addWidget(self.add_item_button)
        layout.addWidget(self.show_all_items_button)
        layout.addWidget(self.search_item_button)
        layout.addWidget(self.item_list_table)
        
        tab.setLayout(layout)
        return tab

    # 创建主界面中的账户管理界面选项卡
    def create_account_management_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        self.logout_button = QPushButton("退出登录")
        self.logout_button.clicked.connect(self.logout)

        self.delete_account_button = QPushButton("注销账号")
        self.delete_account_button.clicked.connect(self.delete_account)
        
        self.admin_channel_button = QPushButton("管理员通道")
        self.admin_channel_button.clicked.connect(self.open_admin_channel)

        layout.addWidget(self.logout_button)
        layout.addWidget(self.delete_account_button)
        layout.addWidget(self.admin_channel_button)

        tab.setLayout(layout)
        return tab

    # 注册用户
    def register_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        address = self.address_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        # 检查输入是否为空
        if not username or not password or not address or not phone or not email:
            QMessageBox.warning(self, '错误', "所有字段不能为空，请完整填写信息！")
            return

        # 检查用户名是否已被占用
        if self.user_manager.is_username_taken(username):
            QMessageBox.warning(self, '错误', "该用户名已被占用，请选择其他用户名。")
            return
        
        # 创建并添加用户
        user = OrdinaryUser(username, password, address, phone, email)
        self.user_manager.add_user(user)

        QMessageBox.information(self, '注册成功', f"{username} 注册成功，等待管理员批准！")
    
    # 注册成为管理员    
    def register_as_admin(self):
        username = self.username_input.text()
        
        # 检查用户名是否已被占用
        if self.user_manager.is_username_taken(username):
            QMessageBox.warning(self, '错误', "该用户名已被占用，请选择其他用户名。")
            return
        
        # 弹出对话框输入邀请码
        dialog = QDialog(self)
        dialog.setWindowTitle("输入邀请码")
        layout = QVBoxLayout()

        self.invite_code_input = QLineEdit()
        submit_button = QPushButton("提交")
        cancel_button = QPushButton("取消")

        layout.addWidget(QLabel("请输入邀请码"))
        layout.addWidget(self.invite_code_input)
        layout.addWidget(submit_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)

        submit_button.clicked.connect(self.check_invite_code)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    # 检查邀请码是否正确
    def check_invite_code(self):
        invite_code = self.invite_code_input.text()

        if invite_code == "SJTUCS3331":
            username = self.username_input.text()
            password = self.password_input.text()
            address = self.address_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()

            user = AdministratorUser(username, password, address, phone, email)
            self.user_manager.add_user(user)
            QMessageBox.information(self, "注册成功", f"{username} 注册成功，您已成为管理员。")
        else:
            QMessageBox.warning(self, "邀请码错误", "邀请码错误！")

    # 用户登录
    def login_user(self):
        username = self.login_username_input.text()
        password = self.login_password_input.text()

        # 检查用户名是否为空
        if not username:
            QMessageBox.warning(self, '错误', "用户名不能为空！")
            return

        # 检查用户是否已经登录
        if self.item_manager.current_user is not None and self.item_manager.current_user.username == username:
            QMessageBox.warning(self, '错误', f"用户 {username} 已经登录，请勿重复登录。")
            return

        # 用户登录验证
        user = self.user_manager.authenticate_user(username, password)

        if user:
            # 检查是否是普通用户且是否被管理员批准
            if isinstance(user, OrdinaryUser) and not user.is_approved:
                QMessageBox.warning(self, '登录失败', f"用户 {username} 尚未被管理员批准，无法登录。")
                return

            self.item_manager.current_user = user
            QMessageBox.information(self, '登录成功', f"欢迎 {username}!")

            # 登录成功后，切换到主界面
            self.stacked_widget.setCurrentWidget(self.main_tab)
        else:
            QMessageBox.warning(self, '登录失败', "用户名或密码错误，请重试。")

    # 退出登录
    def logout(self):
        reply = QMessageBox.question(self, '确认退出',
                                     "你确定要退出登录吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if hasattr(self, 'admin_tab') and self.admin_tab is not None:
                self.tabs.removeTab(2)
                self.admin_tab = None  # 清除管理员选项卡的引用
            self.item_manager.current_user = None
            self.stacked_widget.setCurrentWidget(self.login_tab)
            # 恢复“管理员通道”按钮的可见性
            self.admin_channel_button.setVisible(True)

    # 注销账号
    def delete_account(self):
        reply = QMessageBox.question(self, '确认注销',
                                     "你确定要注销账号吗？",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if hasattr(self, 'admin_tab') and self.admin_tab is not None:
                self.tabs.removeTab(2)
                self.admin_tab = None  # 清除管理员选项卡的引用
            self.user_manager.delete_user(self.item_manager.current_user.username)
            self.stacked_widget.setCurrentWidget(self.registration_tab)
            self.item_manager.current_user = None
            # 恢复“管理员通道”按钮的可见性
            self.admin_channel_button.setVisible(True)

    # 切换到登录界面
    def go_to_login(self):
        self.stacked_widget.setCurrentWidget(self.login_tab)
    
    # 切换到注册界面
    def go_to_register(self):
        self.stacked_widget.setCurrentWidget(self.registration_tab)
    
    # 更新不同物品类型的额外字段
    def update_extra_fields(self):
        # 清除之前的额外字段
        index = 0
        while True:
            item = self.extra_layout.itemAt(index)
            if item is None:  # 如果找不到更多的项
                break
            widget = item.widget()
            if widget:
                widget.deleteLater()
            index += 1

        # 根据物品类型，显示不同的额外属性
        item_type = self.item_type_combo.currentText()
        attributes = self.item_manager.get_item_type_attributes(item_type)

        for attr in attributes:
            input_field = QLineEdit()
            self.extra_layout.addRow(attr, input_field)

        # 确保布局更新以反映更改
        self.extra_layout.update()  # 强制更新布局
        self.extra_layout.parent().update()  # 强制更新父布局

    # 添加物品到物品列表
    def add_item(self):
        # 获取用户输入的物品信息
        item_name = self.item_name_input.text()
        item_description = self.item_description_input.text()
        item_address = self.item_address_input.text()
        item_phone = self.item_phone_input.text()
        item_email = self.item_email_input.text()
        item_type = self.item_type_combo.currentText()

        # 检查是否有空字段
        if not item_name or not item_description or not item_address or not item_phone or not item_email:
            QMessageBox.warning(self, '错误', "所有字段不能为空，请完整填写物品信息！")
            return
        
        # 根据物品类型创建物品属性字典
        item_attributes = {}
        attributes = self.item_manager.get_item_type_attributes(item_type)
        for i, attr in enumerate(attributes):
            input_field = self.extra_layout.itemAt(i*2 + 1).widget()
            item_attributes[attr] = input_field.text()

        item = Item(item_name, item_description, item_address, item_phone, item_email, item_type, item_attributes)

        # 添加物品到物品管理器
        self.item_manager.add_item(item)

        # 展示全部物品
        self.show_all_items()

        # 清空输入框
        self.item_name_input.clear()
        self.item_description_input.clear()
        self.item_address_input.clear()
        self.item_phone_input.clear()
        self.item_email_input.clear()

        # 重置额外属性输入框
        self.update_extra_fields()
    
    # 删除某一件物品    
    def delete_item(self, selected_row):
        if selected_row != -1:
            item_name = self.item_list_table.item(selected_row, 0).text()
            item_owner_name = self.item_list_table.item(selected_row, 6).text()
            if self.item_manager.current_user.username != item_owner_name and not self.item_manager.current_user.is_admin:
                QMessageBox.warning(self, "警告", "普通用户不能删除其他人发布的物品。")
            elif self.item_manager.current_user.username != item_owner_name and self.item_manager.current_user.is_admin:
                self.item_manager.delete_item(item_name)  # 删除物品
                self.show_all_items()  # 更新物品列表
                QMessageBox.information(self, "成功删除", "管理员用户可以删除其他人发布的物品。")
            else:
                self.item_manager.delete_item(item_name)  # 删除物品
                self.show_all_items()  # 更新物品列表
                QMessageBox.information(self, "成功删除", "该物品已成功删除。")
        else:
            QMessageBox.warning(self, "警告", "请选择要删除的物品！")

    # 查询物品对话框
    def search_item_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("查询物品")

        layout = QVBoxLayout()

        # 物品类型选择框
        item_type_combo = QComboBox()
        item_type_combo.addItems(self.item_manager.item_types)

        # 查询字段输入框
        query_input = QLineEdit()

        submit_button = QPushButton("查询")
        cancel_button = QPushButton("取消")

        layout.addWidget(QLabel("选择物品类型"))
        layout.addWidget(item_type_combo)
        layout.addWidget(QLabel("输入查询字段"))
        layout.addWidget(query_input)
        layout.addWidget(submit_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)

        submit_button.clicked.connect(lambda: self.search_item(item_type_combo.currentText(), query_input.text(), dialog))
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    # 执行查询物品
    def search_item(self, item_type, query_text, dialog):
        if not query_text:
            QMessageBox.warning(self, "警告", "请输入查询关键字！")
            return

        # 进行查询
        filtered_items = self.item_manager.search_item(item_type, query_text)

        if filtered_items:
            self.show_items(filtered_items)
        else:
            QMessageBox.information(self, "无结果", "没有找到匹配的物品。")

        dialog.accept()
    
    # 展示全部物品    
    def show_all_items(self):
        all_items = self.item_manager.get_all_items()
        self.show_items(all_items)
    
    # 展示给定的物品列表
    def show_items(self, items):
        self.item_list_table.setRowCount(len(items))  # 设置表格行数
        for row, item in enumerate(items):
            # 设置物品的各项信息
            self.item_list_table.setItem(row, 0, QTableWidgetItem(item.name))
            self.item_list_table.setItem(row, 1, QTableWidgetItem(item.description))
            self.item_list_table.setItem(row, 2, QTableWidgetItem(item.address))
            self.item_list_table.setItem(row, 3, QTableWidgetItem(item.phone))
            self.item_list_table.setItem(row, 4, QTableWidgetItem(item.email))
            self.item_list_table.setItem(row, 5, QTableWidgetItem(item.item_type))
            self.item_list_table.setItem(row, 6, QTableWidgetItem(self.item_manager.current_user.username))

            # 添加“删除”按钮
            delete_button = QPushButton("删除")
            delete_button.clicked.connect(lambda checked, row=row: self.delete_item(row))
            self.item_list_table.setCellWidget(row, 7, delete_button)
    
    # 管理员通道
    def open_admin_channel(self):
        if self.item_manager.current_user and self.item_manager.current_user.is_admin:
            self.admin_tab = self.create_admin_tab()
            self.tabs.addTab(self.admin_tab, "管理员")
        else:
            QMessageBox.warning(self, "权限不足", "您不是管理员，无法访问管理员通道。")

    # 创建主界面中的管理员选项卡
    def create_admin_tab(self):
        
        # 隐藏“管理员通道”按钮，防止重复点击
        self.admin_channel_button.setVisible(False)
        
        tab = QWidget()
        layout = QVBoxLayout()
        
        self.show_all_users_button = QPushButton("展示所有用户")
        self.show_all_users_button.clicked.connect(self.update_user_list)
        
        # 物品类型管理按钮
        self.manage_item_type_button = QPushButton("管理物品类型")
        self.manage_item_type_button.clicked.connect(self.open_item_type_management)

        user_list_table = QTableWidget()
        user_list_table.setColumnCount(7)
        user_list_table.setHorizontalHeaderLabels(["用户名", "地址", "电话", "邮箱", "账户类型", "状态", "操作"])
        
        self.user_list_table = user_list_table  # 保持对user_list_table的引用

        layout.addWidget(self.show_all_users_button)
        layout.addWidget(self.manage_item_type_button)
        layout.addWidget(user_list_table)
        tab.setLayout(layout)

        return tab
    
    # 更新用户列表
    def update_user_list(self):
        # 更新用户列表，展示所有用户
        user_list_table = self.user_list_table
        user_list_table.setRowCount(0)  # 清空当前表格内容

        for user in self.user_manager.get_all_users():
            row = user_list_table.rowCount()
            user_list_table.insertRow(row)
            user_list_table.setItem(row, 0, QTableWidgetItem(user.username))
            user_list_table.setItem(row, 1, QTableWidgetItem(user.address))
            user_list_table.setItem(row, 2, QTableWidgetItem(user.phone))
            user_list_table.setItem(row, 3, QTableWidgetItem(user.email))
            user_list_table.setItem(row, 4, QTableWidgetItem("普通用户" if not user.is_admin else "管理员"))
            user_list_table.setItem(row, 5, QTableWidgetItem("待批准" if isinstance(user, OrdinaryUser) and not user.is_approved else "已批准"))

            if isinstance(user, OrdinaryUser) and not user.is_approved:
                approve_button = QPushButton("批准")
                approve_button.clicked.connect(lambda _, u=user: self.approve_user(u))
                user_list_table.setCellWidget(row, 6, approve_button)

    # 批准普通用户登录
    def approve_user(self, user):
        if isinstance(user, OrdinaryUser):
            self.user_manager.approve_user(user.username)
            QMessageBox.information(self, '成功', f"{user.username} 已经批准成为正式用户。")

            # 在 user_list_table 中找到该用户的行，并更新“状态”列为“已批准”
            for row in range(self.user_list_table.rowCount()):
                if self.user_list_table.item(row, 0).text() == user.username:  # 查找用户名
                    self.user_list_table.setItem(row, 5, QTableWidgetItem("已批准"))  # 更新“状态”列
                    break
    
    # 管理物品类型：添加新的类型或更新新的类型对话框
    def open_item_type_management(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("管理物品类型")
        layout = QVBoxLayout()

        # 输入框
        self.new_item_type_name = QLineEdit()
        self.new_item_type_name.setPlaceholderText("物品类型名称")

        self.new_item_type_attributes = QLineEdit()
        self.new_item_type_attributes.setPlaceholderText("属性列表，用逗号分隔")

        submit_button = QPushButton("提交")
        cancel_button = QPushButton("取消")

        layout.addWidget(QLabel("请输入物品类型名称"))
        layout.addWidget(self.new_item_type_name)
        layout.addWidget(QLabel("请输入属性列表"))
        layout.addWidget(self.new_item_type_attributes)
        layout.addWidget(submit_button)
        layout.addWidget(cancel_button)

        dialog.setLayout(layout)

        submit_button.clicked.connect(self.add_or_update_item_type)
        cancel_button.clicked.connect(dialog.reject)

        dialog.exec_()

    # 添加新的类型或更新新的类型
    def add_or_update_item_type(self):
        type_name = self.new_item_type_name.text()
        attributes = self.new_item_type_attributes.text().split(',')

        if not type_name or not attributes:
            QMessageBox.warning(self, "错误", "物品类型名称和属性不能为空！")
            return

        if type_name in self.item_manager.item_types:
            self.item_manager.update_item_type(type_name, attributes)
            QMessageBox.information(self, "成功", f"物品类型 {type_name} 已更新！")
        else:
            self.item_manager.add_item_type(type_name, attributes)
            QMessageBox.information(self, "成功", f"物品类型 {type_name} 已添加！")
            # 更新物品类型选择框
            self.item_type_combo.addItem(type_name)
        
        # 重新更新额外属性输入框
        self.update_extra_fields()
