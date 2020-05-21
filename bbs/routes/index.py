from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
)

from models.user import User
from . import *
from utils import log

main = Blueprint('index', __name__)
"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后，会写入 session，并且重定向到 /profile
"""


@main.route('/')
def index():
    u = current_user()
    return render_template('index.html', user=u)


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    # 用类方法来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('topic.index'))
    else:
        # 在 session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))


@main.route('/profile')
def profile():
    u = current_user()
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u)
