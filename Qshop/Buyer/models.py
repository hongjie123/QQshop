from django.db import models
from QUser.models import Quser

class BuyCar(models.Model):
    """
    购物车表
    """
    car_user=models.CharField(max_length=32)
    goods_name=models.CharField(max_length=32)
    goods_price=models.FloatField()
    goods_picture=models.ImageField(upload_to="buyer/images")
    goods_number=models.IntegerField()
    goods_total=models.FloatField()
    goods_store=models.IntegerField()
    goods_id=models.IntegerField()


class Pay_order(models.Model):
    """
    订单表

    订单状态：
    0--未支付--买家
    1--未发货--卖家
    2--已发货--卖家
    3--签收/
    4--拒收--买家
    """
    order_id=models.CharField(max_length=32) #订单编号
    order_time=models.DateTimeField(auto_now=True)
    order_number=models.IntegerField() #买入商品的条数
    order_total=models.FloatField(default=0)
    order_state=models.IntegerField(default=0) #订单的状态

    order_user=models.ForeignKey(to=Quser,on_delete=models.CASCADE)#买家

class Order_info(models.Model):
    """
    订单详情表
    """
    order_id = models.ForeignKey(to=Pay_order,on_delete=models.CASCADE)
    goods_name=models.CharField(max_length=32)
    goods_number=models.IntegerField()#每个商品买入的个数
    goods_price=models.FloatField()
    goods_total=models.FloatField(default=0)
    goods_picture=models.CharField(max_length=32)

    order_store=models.ForeignKey(to=Quser,on_delete=models.CASCADE)#卖家


class History(models.Model):
    """
    存储浏览的历史记录
    """
    user_email=models.CharField(max_length=32)
    goods_id=models.IntegerField()
    goods_name=models.TextField()
    goods_price=models.FloatField()
    goods_picture=models.TextField()