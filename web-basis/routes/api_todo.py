import json
from routes.session import session
from utils import (
    log,
)
from routes import (
    redirect,
    http_response,
    json_response,
)
from models.todo import Todo


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    """
    返回所有 todo
    """
    todos = Todo.all()
    # 要转换为 dict 格式才行
    todos = [t.json() for t in todos]
    return json_response(todos)


route_dict = {
    # todo api
    '/api/todo/all': all,
}
