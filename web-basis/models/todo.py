from models import Model


# 定义一个 class 用于保存用户信息
class Todo(Model):
    def __init__(self, form):
        self.id = int(form.get('id', -1))
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
