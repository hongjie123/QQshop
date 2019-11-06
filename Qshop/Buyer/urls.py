from django.contrib import admin
from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [

    re_path(r"^$", index),
    path("index/", index),
    path("login/", login),

    path("goods_list/", list),
    re_path(r"goods/(?P<id>\d+)/", goods),
    path("cart/", cart),
    path("place_order/", place_order),
    path("get_pay/", get_pay),
    path("pay_result/", pay_result),
    path("add_car/", add_car),
    path("user_center_info/", user_center_info),
    path("user_center_site/", user_center_site),
    path("user_center_order/", user_center_order),

]