from routes.session import session
from utils import (
    log,
    template,
)
from routes import (
    redirect,
    http_response,
)


def main_index(request):
    return redirect('/todo/index')


def index(request):
    """
    主页处理函数，返回主页的响应
    """
    body = template('todo_index.html')
    return http_response(body)


route_dict = {
    '/': main_index,
    '/todo/index': index,
}
