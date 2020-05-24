import time
from models import Model


# 定义一个 class 用于保存用户信息
class Todo(Model):
    def __init__(self, form):
        self.id = int(form.get('id', -1))
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        self.ct = int(time.time())  # create time
        self.ut = self.ct  # update time

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 todo 并且返回它
        Todo.new({'task': '吃饭'})
        form: 一个字典 包含了 todo 的数据
        """
        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        t.save()

    @classmethod
    def complete(cls, id, completed):
        """
        用法很方便
        Todo.complete(1, True)
        Todo.complete(2, False)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id
