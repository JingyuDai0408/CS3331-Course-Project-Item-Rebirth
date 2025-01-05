class User:
    def __init__(self, username, password, address, phone, email):
        self.username = username
        self.password = password
        self.address = address
        self.phone = phone
        self.email = email
        self.is_admin = False  # 默认是普通用户

    def promote_to_admin(self):
        self.is_admin = True
        print(f"{self.username} is now an administrator.")

    def __str__(self):
        return f"{self.username} ({'Admin' if self.is_admin else 'Ordinary User'})"


class OrdinaryUser(User):
    def __init__(self, username, password, address, phone, email):
        super().__init__(username, password, address, phone, email)
        self.is_admin = False
        self.is_approved = False  # 是否批准，默认为未批准
    
    def approve(self):
        self.is_approved = True
        print(f"{self.username} has been approved.")

class AdministratorUser(User):
    def __init__(self, username, password, address, phone, email):
        super().__init__(username, password, address, phone, email)
        self.is_admin = True