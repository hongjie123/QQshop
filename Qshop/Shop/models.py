from django.db import models
from ckeditor.fields import RichTextField
from QUser.models import Quser

class GoodsTypeManager(models.Manager):
    def hello(self,id):
        return self.get(id=id).goods_set.all()[:4]

class GoodsType(models.Model):
    name=models.CharField(max_length=32)
    picture = models.ImageField(upload_to="shop/img", default="shop/img/tao.jpg")
    objects=GoodsTypeManager()

class Goods(models.Model):
    name=models.CharField(max_length=32)
    price=models.FloatField()
    number=models.IntegerField()
    production=models.DateTimeField()
    safe_date=models.CharField(max_length=32)
    description = RichTextField()
    picture=models.ImageField(upload_to="shop/img",default="shop/img/tao.jpg")
    statue=models.IntegerField() #0表示下架，1表示在售

    goods_type=models.ForeignKey(to=GoodsType,on_delete=models.CASCADE,default=1)#关联到商品类型表
    goods_store=models.ForeignKey(to=Quser,on_delete=models.CASCADE)#关联到(Quser)即卖家



