from django.contrib import admin
from django.urls import path,re_path
from Shop.views import *

urlpatterns = [
    re_path(r"^$",index),
    path("index/",index),
    path("register/",register),
    path("login/",login),
    path("logout/",logout),
    path("forget_password/",forget_password),
    path("reset_password/",reset_password),
    path("change_password/",change_password),
    path("profile/",profile),
    path("set_profile/",set_profile),
    path("add_goods/",add_goods),
    path("list_goods/",list_goods),
    re_path(r"^update_goods/(?P<id>\d+)/",update_goods),
    re_path(r"^goods/(?P<id>\d+)/",goods),
    re_path(r"^set_goods/(?P<id>\d+)/",set_goods),

    path("Goods/",GoodView.as_view()),
    path("vue_list_goods/",vue_list_goods),
    path("order_list/",order_list),
    path("send_shop/",send_shop),

    path("return_goods_number/",return_goods_number),#用于首页柱状图

]

urlpatterns+=[
    path("get_celery/",get_celery),
    path("base/",base),

    path("test_goods/",test_goods),
    re_path(r"test_goods/(?P<id>\d+)/",test_goods),
]