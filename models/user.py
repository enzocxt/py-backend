from . import Model


class User(Model):
    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @classmethod
    def new(cls, form):
        return cls(form)

    def validate_login(self):
        return self.username == 'gua' and self.password == '123'

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2