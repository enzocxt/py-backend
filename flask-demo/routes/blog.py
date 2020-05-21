from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from models.blog import (
    Blog,
    BlogComment,
)
from utils import log

main = Blueprint('blog', __name__)

"""
1. 拆分有哪些页面 一个页面就可以了
    1.1 发博客 link 点进去以后能进入发博客的页面
    1.2 具体的博客，博客的标题，可以被点击
    2.1 博客正文，作者，title，时间，内容
    2.2 发表评论的窗口，发表的评论，都是针对这个博客的
    2.3 显示所有评论的地方，这里面会有评论
    3.1 创建 blog 的页面

2. 组织哪些数据，把数据的操作实现
blog 数据结构
1. id int
2. author string
3. content string
4. time int

blog 数据的方法
1. 新建博客
2. 根据 blog id 拿到一个 blog

blog comment
1. id int
2. author string
3. comment string
4. time int
5. blog_id 也应该被索引

blog comment 操作
1. new
2. blog_id 查询

数据结构 + 数据方法 => 类

3. 逻辑
    3.1 add 的时候创建 blog，然后跳转 /blog/new 这个页面
    3.2 创建完毕，回到 index
    3.3 点击某个 blog，进入 blog 的详细页
    3.4 在详情页，提交一条评论，跳转回来，显示评论

4，开始实现代码，部分对，部分todo
5，剩下的部分一点点补全
6，美化页面
7，交互
"""


@main.route('/')
def index():
    blogs = Blog.all()
    return render_template('blog.html', blogs=blogs)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    Blog.new(form)
    return redirect(url_for('.index'))


@main.route('/new', methods=['GET'])
def new():
    return render_template('blog_new.html')


@main.route('/<int:blog_id>', methods=['GET'])
def view(blog_id):
    comments = BlogComment.find_all(blog_id=blog_id)
    blog = Blog.find(blog_id)
    return render_template('blog_view.html', blog=blog, comments=comments)


@main.route('/comment/new', methods=['POST'])
def comment():
    form = request.form
    BlogComment.new(form)
    blog_id = form.get('blog_id', -1)
    return redirect(url_for('.view', blog_id=blog_id))
