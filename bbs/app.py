from flask import (
    Flask,
)

import config


# web framework
# web application
# __main__
app = Flask(__name__)
# 设置 secret_key 来使用 flask 自带的 session
# 这个字符串随便你设置什么内容都可以
app.secret_key = config.secret_key


"""
在 flask 中，模块化路由的功能由 蓝图（Blueprints）提供
蓝图可以拥有自己的静态资源路径、模板路径（现在还没涉及）
用法如下
"""
# 注册蓝图
# 有一个 url_prefix 可以用来给蓝图中的每个路由加一个前缀
# TODO: 应该有 登录注册路由，topic 路由，。。。
from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
app.register_blueprint(index_routes)
app.register_blueprint(topic_routes, url_prefix='/topic')
app.register_blueprint(reply_routes, url_prefix='/reply')
app.register_blueprint(board_routes, url_prefix='/board')
"""
1. 拆分有哪些页面 一个页面就可以了
    1.1 首先要有 index 页面，其中有 login, register 路由

2. 组织哪些数据，把数据的操作实现
User 数据结构
1. id int
2. username
3. password
4. time int

User 数据的方法
1. 

数据结构 + 数据方法 => 类

3. 逻辑
    3.1 register 根据 form 数据新建用户（检查用户是否存在，用户名、密码合法性，...）
    3.2 login 登录后跳转到首页

4，开始实现代码，部分对，部分todo
5，剩下的部分一点点补全
6，美化页面
7，交互
"""


"""
上传头像
1. form
2. POST 方法 对应一个路由 保存静态文件的功能
    1. 文件后缀要做过滤 img png gif
    2. 文件名也要小心
3. GET 方法，本地的静态文件转发给用户
"""


# 运行代码
if __name__ == '__main__':
    # debug 模式可以自动加载你对代码的变动, 所以不用重启程序
    # host 参数指定为 '0.0.0.0' 可以让别的机器访问你的代码
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=2000,
    )
    app.run(**config)
