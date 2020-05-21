from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)


from models.comment import Comment
from utils import log

# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
# 第二个参数是套路
main = Blueprint('comment', __name__)


"""
1. 拆分有哪些页面 一个页面就可以了
--- author --- content --- button ---

--- comment ---
--- comment ---
.....

2. 组织哪些数据，把数据的操作实现
comment 数据结构
1. id
2. author string
3. content string
4. time int

comment 数据的方法
1. 新建评论
2. 所有的评论

数据结构 + 数据方法 => 类

3. 逻辑
    3.1 add 的时候增加一个评论，然后跳转回到主页，在主页显示所有评论
    
4，开始实现代码，部分对，部分todo
5，剩下的部分一点点补全
6，美化页面
7，交互
"""


@main.route('/')
def index():
    comments = Comment.all()
    return render_template('comment.html', comments=comments)


@main.route('/add', methods=['POST'])
def add():
    t = Comment.new(request.form)
    return redirect(url_for('.index'))
