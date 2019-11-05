from django.shortcuts import render

import hashlib
from QUser.models import Quser

#加密
def set_password(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result

#效验用户是否存在
def valid_user(email):
    """
        如果email存在，返回数据
        否则返回false
        """
    try:
        user=Quser.objects.get(email=email)
    except Exception as e:
        return False
    else:
        return user

#用户注册函数
def add_user(**kwargs):
    """
        将用户信息保存到数据库
        :return:
    """
    if "email" in kwargs and "username" not in kwargs:
        kwargs["username"]=kwargs["email"]
    user = Quser.objects.create(**kwargs) #? create 什么意思
    return user

def update_user(id,**kwargs):
    pass
def delete_user(id):
    pass





# Create your views here.
