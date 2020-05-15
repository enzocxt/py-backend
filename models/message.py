from . import Model


class Message(Model):
    """
    Message 是用来保存留言的 model
    """
    def __init__(self, form):
        self.author = form.get('author', '')
        self.message = form.get('message', '')
