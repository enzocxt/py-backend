from models import Model


# 定义一个 class 用于保存用户信息
class User(Model):
    def __init__(self, form):
        self.id = int(form.get('id', -1))
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    def hash_password(self, pwd):
        import hashlib
        # 用 ASCII 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    def salted_password(self, password, salt='`~!@#$%^&*()_+-=[]{};:,./?><'):
        # hash the concatenate string of hashed password with salt
        hash1 = self.hash_password(password)
        hash2 = self.hash_password(hash1 + salt)
        return hash2

    def validate_login(self):
        # 暂时做最简单的验证
        u = User.find_by(username=self.username)
        return u is not None and self.password == u.password

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2
