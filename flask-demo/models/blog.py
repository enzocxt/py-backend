import time

from . import Model


class Blog(Model):
    def __init__(self, form):
        self.id = None
        self.author = form.get('author', '')
        self.title = form.get('title', '')
        self.content = form.get('content', '')
        self.ct = int(time.time())


class BlogComment(Model):
    def __init__(self, form):
        self.id = None
        self.content = form.get('content', '')
        self.author = form.get('author', '')
        self.blog_id = int(form.get('blog_id', -1))
        self.ct = int(time.time())
