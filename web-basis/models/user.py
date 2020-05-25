from models import Model


# 定义一个 class 用于保存用户信息
class User(Model):
    def __init__(self, form):
        self.id = int(form.get('id', -1))
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def hash_password(pwd):
        import hashlib
        # 用 ASCII 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    def salt_password(self, password, salt='`~!@#$%^&*()_+-=[]{};:,./?><'):
        # hash the concatenate string of hashed password with salt
        hash1 = self.hash_password(password)
        hash2 = self.hash_password(hash1 + salt)
        return hash2

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.salt_password(self.password)

    def validate_register(self):
        pwd = self.password
        self.password = self.salt_password(pwd)
        if User.find_by(username=self.username) is None:
            self.save()
            return self
        else:
            return None
