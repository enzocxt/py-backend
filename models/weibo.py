from . import Model
from .todo import Todo
from .comment import Comment


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = form.get('id', None)
        if self.id is not None:
            self.id = int(self.id)
        self.content = form.get('content', '')
        self.user_id = form.get('user_id', user_id)

    def comments(self):
        return Comment.find_all(weibo_id=self.id)
