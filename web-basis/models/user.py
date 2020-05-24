from models import Model


# 定义一个 class 用于保存用户信息
class User(Model):
    def __init__(self, form):
        self.id = int(form.get('id', -1))
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def validate_login(self):
        # 暂时做最简单的验证
        u = User.find_by(username=self.username)
        return u is not None and self.password == u.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
