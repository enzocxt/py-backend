import os
from werkzeug.utils import secure_filename
from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)

from models.user import User
from . import *
from utils import log
from config import user_file_directory

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


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


@main.route('/addimg', methods=['POST'])
def add_img():
    u = current_user()
    # Flask 套路：
    # 表单提交的 img 会存在 request.files 中
    # 然后根据表单中的 name 作为 key 获得对象
    # request.files['file']
    if u is None:
        return redirect(url_for('.profile'))
    if 'file' not in request.files:
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        return redirect(request.url)
    if allow_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(user_file_directory, filename))
        u.user_image = filename
        u.save()
    return redirect(url_for('.profile'))


# send_from_directory
# nginx 静态文件
@main.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(user_file_directory, filename)
