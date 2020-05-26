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

    def json(self):
        d = self.__dict__.copy()
        comments = [c.json() for c in self.comments()]
        d['comments'] = comments
        return d

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 weibo 并且返回它
        Weibo.new({'content': '吃饭'})
        form: 一个字典 包含了 weibo 的数据
        """
        m = cls(form, user_id=user_id)
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        m = cls.find(id)
        valid_names = [
            'content'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(m, key, form[key])
        # 更新修改时间
        m.ut = int(time.time())
        m.save()
        return m


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
