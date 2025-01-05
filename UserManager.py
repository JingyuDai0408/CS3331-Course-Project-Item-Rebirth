from User import OrdinaryUser
class UserManager:
    def __init__(self):
        self.users = []
    
    def add_user(self, user):
        self.users.append(user)

    def get_all_users(self):
        return self.users
    
    def authenticate_user(self, username, password):
        user = next((u for u in self.users if u.username == username and u.password == password), None)
        return user
    
    def delete_user(self, username):
        """删除指定用户名的用户"""
        user_to_delete = self.get_user_by_username(username)
        if user_to_delete:
            self.users.remove(user_to_delete)
            return True
        return False
    
    def get_user_by_username(self, username):
        """根据用户名获取用户"""
        for user in self.users:
            if user.username == username:
                return user
        return None
    
    def approve_user(self, username):
        # 批准普通用户为管理员
        for user in self.users:
            if isinstance(user, OrdinaryUser) and user.username == username:
                user.is_approved = True
                user.approve()
                break
    
    def is_username_taken(self, username):
        # 检查用户名是否已存在
        return any(u.username == username for u in self.users)