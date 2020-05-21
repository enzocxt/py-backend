from utils import (
    log,
    template,
    redirect,
    http_response,
)
from .session import session


def main_index(request):
    return redirect('/routes/index')


def index(request):
    """
    routes 首页的路由函数
    """
    body = template('todo_index.html')
    return http_response(body)


# 路由字典
route_dict = {
    '/': main_index,
    '/routes/index': index,
}