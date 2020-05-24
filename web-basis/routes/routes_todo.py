from utils import log
from models.user import User
from models.todo import Todo
from . import (
    random_str,
    template,
    redirect,
    response_with_headers,
    current_user,
)


def index(request):
    """
    todo 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    # 找到当前登录的用户, 如果没登录, 就 redirect 到 /login
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    # if u is None:
    #     return redirect('/login')
    # todo_list = Todo.find_all(user_id=u.id)
    todo_list = Todo.all()
    todo_html = ''.join(['<h3>{} : {} </h3>'.format(t.id, t.title)
                         for t in todo_list])
    # todos = []
    # for t in todo_list:
    #     edit_link = '<a href="/todo/edit?id={}">编辑</a>'.format(t.id)
    #     delete_link = '<a href="/todo/delete?id={}">删除</a>'.format(t.id)
    #     s = '<h3>{} : {} {} {}</h3>'.format(t.id, t.title, edit_link, delete_link)
    #     todos.append(s)
    # todo_html = ''.join(todos)
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
    # uname = current_user(request)
    # u = User.find_by(username=uname)
    if request.method == 'POST':
        # 'title=aaa' ==> {'title': 'aaa'}
        form = request.form()
        t = Todo.new(form)
        # t.user_id = u.id
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/todo')


def edit():
    ...


route_dict = {
    '/todo': index,
    '/todo/add': add,
}
