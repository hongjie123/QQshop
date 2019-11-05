from django.db import models


# Create your models here.

class Quser(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=32)

    username = models.CharField(max_length=32, blank=True, null=True)
    gender = models.CharField(max_length=8, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    phone = models.CharField(max_length=32, blank=True, null=True)
    address = models.TextField(blank=True, null=True)  # 用户的籍贯
    picture = models.ImageField(upload_to="image", default="image/photo.jpg")
    identity = models.IntegerField(default=0)  # 0代表买家，1代表卖家，2代表平台


class GoodsAddress(models.Model):
    """
    收货地址
    """

    recver = models.CharField(max_length=32)  # 收件人
    address=models.TextField() #详细地址
    post_number = models.CharField(max_length=32)  # 邮编地址
    phone = models.CharField(max_length=32)
    state = models.IntegerField()  # 0常规地址，1当前地址

    user = models.ForeignKey(to=Quser, on_delete=models.CASCADE)  # 关联到(Quser)即卖家；一个用户可以有多个收货地址
