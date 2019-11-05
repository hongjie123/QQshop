from django import template
from Shop.models import *

register=template.Library() #实例化Django模板库

@register.filter #注册过滤器
def get_four(obj): #过滤器方法
    return obj[:4]

@register.filter #注册过滤器
def get_filter(obj): #过滤器方法
    """
    :param obj: 是一个查询商品实例对象
    :return:
    """
    result=obj.goods_set.filter(statue=1)[:4]
    return result

@register.filter
def uper(obj):
    return obj.upper()

@register.filter
def jq(obj):
    result=obj.replace("/media/","")
    return result

@register.filter("set_phone")
def set_phone(obj):
    result=obj[:3]+"****"+obj[7:]
    return result


