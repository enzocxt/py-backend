import hashlib

from . import Model
from .todo import Todo


class User(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod
    def salted_password(password, salt='~!@#$%^&*()_+[]{}\|<>?'):
        """~!@#$%^&*()_+[]{}\|<>?"""
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()
        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    def validate_login(self):
        u = User.find_by(username=self.username)
        return u is not None and u.password == self.salted_password(self.password)

    def validate_register(self):
        pwd = self.password
        self.password = self.salted_password(pwd)
        if User.find_by(username=self.username) is None:
            self.save()
            return self
        else:
            return None

    def todos(self):
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts
