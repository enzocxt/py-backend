import time
from models import Model
from .user import User


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = int(form.get('id', -1))
        self.content = form.get('content', '')
        self.user_id = int(form.get('user_id', user_id))
        self.ct = int(time.time())  # create time
        self.ut = self.ct  # update time

    def comments(self):
        return Comment.find_all(weibo_id=self.id)


class Comment(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.weibo_id = int(form.get('weibo_id', -1))

    def user(self):
        u = User.find(self.user_id)
        return u
