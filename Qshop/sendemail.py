import smtplib
from email.mime.text import MIMEText

content="""
    我是一个远方的笔友！
"""

sender="2276473611@qq.com"
recver="306957934@qq.com"
password="bevqixdezgzbeafh"

#构建邮件格式
message=MIMEText(content,"plain","utf-8")
message["TO"]=recver
message["From"]=sender
message["Subject"]="浪"

#发送邮件
smtp=smtplib.SMTP_SSL("smtp.qq.com",465)
smtp.login(sender,password)
#recver以列表的形式
smtp.sendmail(sender,recver,message.as_string())
smtp.close()
