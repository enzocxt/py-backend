import time
from . import Model


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.views = 0
        self.title = form.get('title', '')
        self.ct = int(time.time())
        self.ut = self.ct
