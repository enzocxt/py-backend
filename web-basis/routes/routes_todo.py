from utils import log
from models.user import User
from models.todo import Todo
from . import (
    random_str,
    template,
    redirect,
    response_with_headers,
)
from .routes_index import current_user


"""
routes/todo
    显示所有 todo
    增加 todo
    编辑 todo
    删除 todo
models/todo
    todo 数据 class
templates/todo
    todo_index.html
    todo_edit.html
    
点击添加按钮增加一个新的 todo 的时候，程序流程如下：
1. 浏览器提交一个表单给服务器（POST 请求）
POST /todo/add HTTP/1.1
Content-Type: application/x-www-form-urlencoded

title=xxx

2. 服务器解析表单数据，并增加一条新数据，并返回 302 响应
HTTP/1.1 302 REDIRECT
Location: /todo

3. 浏览器根据 302 中的地址（Location），发送一条新的 GET 请求
GET /todo HTTP/1.1
Host: xxx

4. 服务器给浏览器一个页面响应
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: ...

<html>
...
</html>

5. 浏览器把新的页面显示出来


TODO 带用户验证功能
"""


def index(request):
    """
    todo 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_list = Todo.find_all(user_id=u.id)
    todos = []
    for t in todo_list:
        edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
        delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
        s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
        todos.append(s)
    todo_html = ''.join(todos)
    # 替换模板文件中的标记字符串
    body = template('todo_index.html')
    body = body.replace('{{todos}}', todo_html)
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        t = Todo.new(form)
        t.user_id = u.id
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def edit(request):
    """
    todo edit 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 todo 的 id
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    # 权限
    if t.user_id != u.id:
        return redirect('/login')
    # if todo_id < 1:
    #     return error(404)
    # 替换模板文件中的标记字符串
    body = template('todo_edit.html')
    body = body.replace('{{todo_id}}', str(t.id))
    body = body.replace('{{todo_title}}', str(t.title))
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def update(request):
    """
    用于更新 todo 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        todo_id = int(form.get('id', -1))
        t = Todo.find_by(id=todo_id)
        t.title = form.get('title', t.title)
        t.save()
    return redirect('/todo')


def delete(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/todo')


route_dict = {
    # GET 请求，显示页面
    '/todo': index,
    '/todo/edit': edit,
    # POST 请求，处理数据
    '/todo/add': add,
    '/todo/update': update,
    '/todo/delete': delete,
}
