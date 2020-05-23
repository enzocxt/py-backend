from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    abort,
)

from routes import *
from models.mail import Mail


main = Blueprint('mail', __name__)


@main.route('/')
def index():
    # 找出所有的 收 发 信息 并渲染出来
    u = current_user()
    sent_mails = Mail.find_all(sender_id=u.id)
    received_mails = Mail.find_all(receiver_id=u.id)
    return render_template('mail/index.html', sends=sent_mails, receives=received_mails)


@main.route('/add', methods=['POST'])
def add():
    form = request.form
    mail = Mail.new(form)
    # 为了安全起见，需要把自己当做 sender 设置进去
    u = current_user()
    mail.set_sender(u.id)
    return redirect(url_for('.index'))


@main.route('/view/<int:id>')
def view(id):
    mail = Mail.find(id)
    # 不是你自己收发的，你肯定不能看
    # 不是接受者，那你看了也不会变成已读
    u = current_user()
    if u.id == mail.receiver_id:
        mail.mark_read()
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template("mail/detail.html", mail=mail)
    else:
        return redirect(url_for('.index'))
