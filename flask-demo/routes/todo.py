from flask import (
    render_template,
    request,
    flash,
    redirect,
    url_for,
    Blueprint,
)

from models.todo import Todo


# 创建一个 蓝图对象 并且路由定义在蓝图对象中
# 然后在 flask 主代码中「注册蓝图」来使用
# 第一个参数是蓝图的名字, 以后会有用(add函数里面就用到了)
# 第二个参数是套路
main = Blueprint('todo', __name__)


@main.route('/')
def index():
    # 查找所有的 routes 并返回
    todo_list = Todo.all()
    # flask 已经配置好了 jinjia2 模板引擎
    # 并且可以直接使用 render_template 来生成相应数据（http_response）
    return render_template('todo_index.html', todos=todo_list)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    t = Todo.new(form)
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 routes
    return redirect(url_for('todo.index'))


@main.route('/delete/<int:todo_id>/')
def delete(todo_id):
    """
    <int:todo_id> 的方式可以匹配一个 int 类型
    int 指定了它的类型，省略的话参数中的 todo_id 就是 str 类型

    这个概念叫做 动态路由
    意思是这个路由函数可以匹配一系列不同的路由

    动态路由是现在流行的路由设计方案
    """
    # 通过 id 删除 routes
    t = Todo.delete(todo_id)
    # 引用蓝图内部的路由函数的时候，可以省略名字只用 .
    # 因为我们就在 routes 这个蓝图里面, 所以可以省略 routes
    # return redirect(url_for('todo.index'))
    return redirect(url_for('.index'))
