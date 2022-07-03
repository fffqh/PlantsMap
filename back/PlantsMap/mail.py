import flask_mail
from flask import Flask, current_app
from threading import Thread

from PlantsMap.extensions import mail_obj

# 异步发送邮件
def send_async_email(app, msg):
    with app.app_context():
        mail_obj.send(msg)


def send_mail(to, subject, template, **kwargs):
    """
    :param to: 收件人
    :param subject: 标题名
    :param template: 验证码，之后可以把字符串验证码改为页面
    :param kwargs: 页面参数
    :return:
    """
    # 获取原始app实例
    app1 = current_app._get_current_object()
    # 创建邮件对象
    msgobject = flask_mail.Message(
        subject,
        body="示例邮件的内容",
        sender=app1.config['MAIL_USERNAME'],
        recipients=[to]
    )
    # 浏览器接受显示内容
    # msgobject.html = render_template('email/' + template + '.html', **kwargs)

    # 终端接受显示内容
    # msgobject.body = render_template('email/' + template + '.html', **kwargs)
    msgobject.body = template

    # send_async_email(app, msg=msgobject)
    # 使用多线程，先响应请求，再进行与smtp的调用
    thr = Thread(target=send_async_email, args=[app1, msgobject])
    thr.start()
    return thr
