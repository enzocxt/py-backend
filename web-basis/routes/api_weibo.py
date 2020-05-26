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
from models.weibo import Weibo


# 本文件只返回 json 格式的数据
# 而不是 html 格式的数据
def all(request):
    """
    返回所有 weibo
    """
    ms = Weibo.all()
    # 要转换为 dict 格式才行
    ms = [m.json() for m in ms]
    print(ms)
    return json_response(ms)


def add(request):
    """
    接收浏览器发来的添加 weibo 请求
    添加数据并返回给浏览器
    """
    # 得到浏览器发送的 json 格式数据
    # 浏览器用 ajax 发送 json 格式的数据过来
    # 所以这里我们用新增加的 json 函数来获取格式化后的 json 数据
    form = request.json()
    # 创建一个 model
    m = Weibo.new(form)
    # 把创建好的 model 返回给浏览器
    return json_response(m.json())


def delete(request):
    """
    通过下面这样的链接来删除一个 weibo
    /delete?id=1
    """
    weibo_id = int(request.query.get('id'))
    w = Weibo.delete(weibo_id)
    return json_response(w.json())


def update(request):
    form = request.json()
    weibo_id = int(form.get('id'))
    w = Weibo.update(weibo_id, form)
    return json_response(w.json())


route_dict = {
    # weibo api
    '/api/weibo/all': all,
    '/api/weibo/add': add,
    '/api/weibo/delete': delete,
    '/api/weibo/update': update,
}
