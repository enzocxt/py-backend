from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    session,
)


main = Blueprint('session', __name__)
"""
1, 拆分有哪些页面，view
2，组织哪些数据，把数据的操作实现
3，逻辑
    3.1 没有登录的时候，直接到登录
    3.2 登录后，要展现出 username 页面
    3.3 当我退出后，回到开始的页面，继续登录
4，开始实现代码，部分对，部分todo
5，剩下的部分一点点补全
6，美化页面
"""


@main.route('/')
def index():
    username = session.get('username', None)
    if username is None:
        return render_template('login.html')
    else:
        return render_template('session_index.html', username=username)


@main.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '')
    session['username'] = username
    return redirect(url_for('.index'))


@main.route('/logout', methods=['GET'])
def logout():
    session.pop('username')
    return redirect(url_for('.index'))
