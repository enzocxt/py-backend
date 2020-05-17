
from utils import log
from utils import template
from utils import redirect
from utils import http_response
from models.todo import Todo
from . import redirect
from . import response_with_headers


def index(request):
    """
    todo 首页的路由函数
    """
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)


def add(request):
    """
    用于增加新 todo 的路由函数
    """
    # 得到浏览器发送的表单
    form = request.form()
    # 创建一个 todo
    Todo.new(form)
    # 让浏览器刷新页面到主页去
    return redirect('/')


def edit(request):
    """
    edit 首页的路由函数，返回 edit 页的响应
    /edit?id=1
    """
    todo_id = int(request.query.get('id', -1))
    t = Todo.find_by(id=todo_id)
    body = template('simple_todo_edit.html', todo=t)
    return http_response(body)


def update(request):
    form = request.form()
    # todo_id = int(request.query.get('id'))
    todo_id = int(form.get('id'))
    Todo.update(todo_id, form)
    return redirect('/')


def delete(request):
    """
    通过下面这样的链接来删除一个 todo
    /delete?id=1
    """
    todo_id = int(request.query.get('id'))
    Todo.delete(todo_id)
    return redirect('/')


# 路由字典
route_dict = {
    '/': index,
    '/add': add,
    '/edit': edit,
    '/update': update,
    '/delete': delete,
}