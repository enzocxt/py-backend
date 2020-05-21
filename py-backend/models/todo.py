import time
from . import Model


# 继承自 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        # self.task = form.get('task', '')
        self.title = form.get('title', '')
        self.task = self.title
        self.completed = False
        # 和别的数据关联的方式，用 user_id 表明拥有它的 user 实例
        self.user_id = int(form.get('user_id', user_id))
        # 还应该增加 时间 等数据
        self.ct = int(time.time())  # create time
        self.ut = self.ct  # update time

    @classmethod
    def new(cls, form, user_id=-1):
        """
        创建并保存一个 routes 并且返回它
        Todo.new({'task': '吃饭'})
        :param form: 一个字典 包含了 routes 的数据
        :return: 创建的 routes 实例
        """
        # 下面一行相当于 t = Todo(form)
        t = cls(form, user_id)
        t.save()
        return t

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            # 'task',
            'title',
            'completed'
        ]
        for key in form:
            # 这里只应该更新我们想要更新的东西
            if key in valid_names:
                setattr(t, key, form[key])
        # 更新修改时间
        t.ut = int(time.time())
        t.save()
        return t

    @classmethod
    def complete(cls, id, completed=True):
        """
        用法很方便
        Todo.complete(1)
        Todo.complete(2, False)
        """
        t = cls.find(id)
        t.completed = completed
        t.save()
        return t

    def is_owner(self, id):
        return self.user_id == id

