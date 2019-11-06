from django.shortcuts import render,HttpResponseRedirect
from django.http import JsonResponse

from Shop.models import *
from QUser.views import valid_user,set_password
from Buyer.models import *
# 校验登录
def login_valid(fun):
    def inner(request, *args, **kwargs):
        referer=request.GET.get("referer")#证明使用者的目的地在购物车页面
        cookie_user = request.COOKIES.get("email")
        session_user = request.session.get("email")
        if cookie_user and session_user and cookie_user == session_user:
            return fun(request, *args, **kwargs)
        else:
            login_url="/Buyer/login/"
            if referer:
                login_url="/Buyer/login/?referer=%s"%referer
            return HttpResponseRedirect(login_url)

    return inner


def login(request):
    #记录登录请求是从哪里到的登录页面
    referer=request.GET.get("referer")#获取url上带的特殊要求（要去的目的地）
    if not referer:
        referer=request.META.get("HTTP_REFERER")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("pwd")
        # 判断用户是否存在
        # 如果存在
        user = valid_user(email)  # 返回值不懂
        if user:
            # 判断密码是否正确
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                if request.POST.get("referer"):
                    referer = request.POST.get("referer")
                if referer in ('http://127.0.0.1:8000/Buyer/login/',"None"):
                    referer = "/"
                response = HttpResponseRedirect(referer)
                # response = HttpResponseRedirect("/Buyer/cart/")
                response.set_cookie("email", user.email)
                response.set_cookie("user_id", user.id)
                response.set_cookie("picture", user.picture)
                request.session["email"] = user.email
                return response
            else:
                error = "密码错误！"
        else:
            error = "用户不存在！"
    return render(request,"buyer/login.html",locals())


def index(request):
    #获取所有类型
    type_list=GoodsType.objects.all()
    #获取单条类型
    type_data=GoodsType.objects.get(id=1)
    #获取对应类型的所有数据
    type_data.goods_set.all()
    #查询每个类型对应的商品
    for t in type_list:
        goods_list=t.goods_set.all()
        # four_goods = GoodsType.objects.hello(t.id)
    #查询每个类型对应的4个商品
    for t in type_list:
        goods_list=t.goods_set.all()[:4]
    #上述内容整理
    #列表推导式
    # result=[{t.name:t.goods_set.all(),"picture":t.picture} for t in type_list]
    result=[{t.name:t.goods_set.all(),"picture":t.picture} for t in type_list]
    meages="hello"


    return render(request,"buyer/index.html",locals())

def list(request):
    id=request.GET.get("id")
    goods_list=Goods.objects.all()
    if id:
        goods_type=GoodsType.objects.get(id=int(id))
        goods_list=goods_type.goods_set.filter(statue=1)

    return render(request, "buyer/goods_list.html",locals())

def goods(request,id):
    goods_data=Goods.objects.get(id=(id))
    email=request.COOKIES.get("email")
    if email:
        now_data=History.objects.filter(user_email=email).order_by("id")
        if len(now_data)>=5:
            now_data[0].delete()
        history=History()
        history.user_email=email
        history.goods_id=id
        history.goods_name=goods_data.name
        history.goods_price=goods_data.price
        history.goods_picture=goods_data.picture
        history.save()
    return render(request, "buyer/goods.html",locals())


@login_valid
def cart(request): #购物车
    email=request.COOKIES.get("email")#获取用户邮箱
    good_list=BuyCar.objects.filter(car_user=email)#获取用户邮箱对应的购物车数据
    count=len(good_list)#购物车商品的数量
    if request.method=="POST": #为了接收提交订单
        #对订单的处理
        data=request.POST
        post_data=[]
        ##过滤所有选择的商品的id和购买数量
        for key in data:
            if key.startswith("check"):
                id=key.split("_")[1]
                num="number_%s"%id
                number=data[num]
                post_data.append((id,number))
        #保存订单主表
        p_order=Pay_order()
        p_order.order_id=str(time.time()).replace(".","")
        p_order.order_number=len(post_data)
        p_order.order_user=Quser.objects.get(email=request.COOKIES.get("email"))
        p_order.save() #这里没有保存总价

        order_total=0 #总价计算
        # 循环保存当前订单对应的订单详情
        for id,number in post_data:
            number=int(number)
            good=Goods.objects.get(id=int(id))
            o_info=Order_info()
            o_info.order_id=p_order #不是很懂
            o_info.goods_name=good.name
            o_info.goods_number=number
            o_info.goods_price=good.price
            o_info.goods_total=number*good.price
            o_info.goods_picture=good.picture.url
            o_info.order_store=good.goods_store
            o_info.save()
            order_total+=o_info.goods_total
        p_order.order_total=order_total #保存当前订单的总价
        p_order.save()
        return HttpResponseRedirect("/Buyer/place_order/?order_id=%s"%p_order.order_id)
    return render(request,"buyer/cart.html",locals())

def place_order(request):
    order_id=request.GET.get("order_id")
    email = request.COOKIES.get("email")
    user = Quser.objects.get(email=email)
    addr = user.goodsaddress_set.filter()
    if order_id:
        p_order=Pay_order.objects.get(order_id=order_id) #订单信息
        order_data=p_order.order_info_set.all() #详情信息
    return render(request,"buyer/place_order.html",locals())


import time
from Buyer.Pay import Pay
def get_pay(request):
    order_number=request.GET.get("order_id")
    order_money=request.GET.get("order_total")
    url=Pay(order_number,order_money)
    return HttpResponseRedirect(url)

def pay_result(request):
    data = request.GET #订单的详细数据

    order_id=request.GET.get("out_trade_no")
    p_order=Pay_order.objects.get(order_id=order_id)
    p_order.order_state=1 #改变订单的状态，改为（已支付）
    p_order.save()
    return render(request,"buyer/pay_result.html",locals())

#添加商品到购物车
def add_car(request):
    result={"state":"error","data":""}
    if request.method=="POST":
        user=request.COOKIES.get("email")
        goods_id=request.POST.get("goods_id")
        number=request.POST.get("number",1)
        try:
            goods=Goods.objects.get(id=goods_id)
        except Exception as e:
            result["data"]=str(e)
        else:
            car=BuyCar()
            car.car_user=user
            car.goods_name=goods.name
            car.goods_picture=goods.picture
            car.goods_price=goods.price
            car.goods_number=number
            car.goods_total=int(number)*goods.price
            car.goods_store=goods.goods_store.id
            car.goods_id=goods.id
            car.save()
            result["state"]="cuccess"
            result["data"]="加入购物车成功"
    return JsonResponse(result)


#个人中心
def user_center_info(request):
    email=request.COOKIES.get("email")
    user_info=Quser.objects.get(email=email)
    goods_his=History.objects.filter(user_email=email)
    return render(request,"buyer/user_center_info.html",locals())

#个人收件地址
from QUser.models import GoodsAddress
def user_center_site(request):
    email=request.COOKIES.get("email")
    user=Quser.objects.get(email=email)
    addr=user.goodsaddress_set.filter(state=1)[0]
    if request.method=="POST":
        recv=request.POST.get("recv")
        address=request.POST.get("address")
        post_number=request.POST.get("post_number")
        phone=request.POST.get("phone")

        addr=GoodsAddress()
        addr.recver=recv
        addr.address=address
        addr.post_number=post_number
        addr.state=0 #添加收件地址的时候设置为常规地址
        addr.recver=recv
        addr.user=user
        addr.save()

    return render(request, "buyer/user_center_site.html", locals())


def user_center_order(request):
    email=request.COOKIES.get("email") #获取cookies中的email
    user=Quser.objects.filter(email=email).first() #通过email获取对应的用户
    if user:
        order_list=user.pay_order_set.all() #获取对应的订单
    return render(request,"buyer/user_center_order.html",locals())

