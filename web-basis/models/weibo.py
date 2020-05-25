import time
from models import Model


class Weibo(Model):
    def __init__(self, form, user_id=-1):
        self.id = int(form.get('id', -1))
        self.content = form.get('content', '')
        self.user_id = int(form.get('user_id', user_id))
        self.ct = int(time.time())  # create time
        self.ut = self.ct  # update time
