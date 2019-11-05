from __future__ import absolute_import
from Qshop.celery import app
#邮件
from Qshop.settings import MAIL_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT,MAIL_USER
import smtplib
from email.mime.text import MIMEText
from email.header import Header

@app.task
def add():
    x=1
    y=2
    return x+y

@app.task
def sendMail(content,email):
    # content1='发邮件测试异步'
    # email="2276473611@qq.com"
    # 第三方 SMTP 服务

    # receivers = email  # 接收邮件，可设置为自己的邮箱或者其他邮箱
    subject = '远方的问候！'
    # content = """
    #         如果确认是本人修改密码，请点击下方链接进行修改密码，
    #         <a href="%s">点击链接确认</a>
    #     """ % content

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(MAIL_SENDER, 'utf-8')
    message['To'] = Header(email, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(MAIL_SERVER, 25)  # 25 为 SMTP 端口号
        smtpObj.login(MAIL_USER, MAIL_PASSWORD)
        smtpObj.sendmail(MAIL_SENDER,email, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException  as e:
        print(e)


