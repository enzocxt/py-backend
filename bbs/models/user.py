import time

from . import Model


class User(Model):
    """
    User 的数据有：id, username, password, create time, update time 等
    操作有：hash，加盐，注册，验证登录
    """
    def __init__(self, form):
        self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.ct = int(time.time())

    @staticmethod
    def hashed_password(pwd):
        import hashlib
        # 用 ASCII 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    def salted_password(self, pwd, salt='~!@#$%^&*()_+-={}[]|;:,./<>?'):
        hash1 = self.hashed_password(pwd)
        hash2 = self.hashed_password(hash1 + salt)
        return hash2

    @classmethod
    def register(cls, form):
        username = form.get('username', '')
        password = form.get('password', '')
        if len(username) > 2 and User.find_by(username=username) is None:
            u = User.new(form)
            u.password = u.salted_password(password)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None
