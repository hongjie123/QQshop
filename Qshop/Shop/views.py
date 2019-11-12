from django.shortcuts import render
from django.http import HttpResponseRedirect
from  QUser.views import *
from Shop.models import *
# 邮件
from Qshop.settings import MAIL_SENDER, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT, MAIL_USER
import smtplib
from email.mime.text import MIMEText
from email.header import Header


# def sendMail(content,email):
#
#     content = """
#         如果确认是本人修改密码，请点击下方链接进行修改密码，
#         <a href="%s">点击链接确认</a>
#     """%content
#     print(content)
#
#     # 构建邮件格式
#     message = MIMEText(content, "html", "utf-8")
#     message["TO"] = email
#     message["From"] = MAIL_SENDER
#     message["Subject"] = "密码修改"
#
#     # 发送邮件
#     smtp = smtplib.SMTP_SSL(MAIL_SERVER, MAIL_PORT)
#     smtp.login(MAIL_SENDER, MAIL_PASSWORD)
#     # recver以列表的形式
#     smtp.sendmail(MAIL_SENDER, [email], message.as_string())
#     smtp.close()

def sendMail(content, email):
    # 第三方 SMTP 服务

    # receivers = email  # 接收邮件，可设置为自己的邮箱或者其他邮箱
    subject = 'Python SMTP 邮件测试'
    content = """
            如果确认是本人修改密码，请点击下方链接进行修改密码，
            <a href="%s">点击链接确认</a>
        """ % content

    message = MIMEText(content, 'plain', 'utf-8')
    message['From'] = Header(MAIL_SENDER, 'utf-8')
    message['To'] = Header(email, 'utf-8')
    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(MAIL_SERVER, 25)  # 25 为 SMTP 端口号
        smtpObj.login(MAIL_USER, MAIL_PASSWORD)
        smtpObj.sendmail(MAIL_SENDER, email, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException  as e:
        print(e)


# 校验登录
def login_valid(fun):
    def inner(request, *args, **kwargs):
        cookie_user = request.COOKIES.get("email")
        session_user = request.session.get("email")
        if cookie_user and session_user and cookie_user == session_user:
            user = Quser.objects.get(email=cookie_user)
            identity = user.identity
            if identity >= 1:
                return fun(request, *args, **kwargs)
            else:
                return HttpResponseRedirect("/")
        else:
            return HttpResponseRedirect("/Shop/login/")

    return inner


def register(request):
    # 后台卖家注册功能
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 检测用户是否注册过
        # 注册过，提示当前邮箱已经注册
        error = ""
        if valid_user(email):
            error = "当前邮箱已经注册"
            # 没有注册过
        else:
            # 对密码加密
            password = set_password(password)
            # 添加到数据库
            add_user(email=email, password=password)
            # 跳转到登录
            return HttpResponseRedirect("/Shop/login/")
    return render(request, "shop/register.html/", locals())


def login(request):
    # 后台卖家登录功能
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # 判断用户是否存在
        # 如果存在
        user = valid_user(email)  # 返回值不懂
        if user:
            # 判断密码是否正确
            db_password = user.password
            request_password = set_password(password)
            if db_password == request_password:
                response = HttpResponseRedirect("/Shop/")
                response.set_cookie("email", user.email)
                response.set_cookie("user_id", user.id)
                response.set_cookie("picture", user.picture)
                request.session["email"] = user.email
                return response
            else:
                error = "密码错误！"
        else:
            error = "用户不存在！"
    return render(request, "shop/login.html", locals())


def logout(request):
    # 后台卖家退出登录功能
    response = HttpResponseRedirect("/Shop/login/")
    response.delete_cookie("email")
    response.delete_cookie("user_id")
    request.session.clear()
    return response


# 用装饰器，限制不登录直接进入首页
@login_valid
def index(request):
    # 后台卖家首页
    email=request.COOKIES.get("email")
    user=Quser.objects.get(email=email)
    #货物种类
    goods_type_count=user.goods_set.all().count() #计数

    return render(request, "shop/index.html", locals())

#用于柱状图和饼图
def return_goods_number(request):
    result={"goods_name":[],"goods_number":[],"goods_list":[]}
    id=request.GET.get("id")
    if id:
        user=Quser.objects.get(id=id)
        goods=user.goods_set.order_by("number")[:6] #计数
        for i in goods:
            result["goods_name"].append(i.name)
            result["goods_number"].append(i.number)
            result["goods_list"].append({"name":i.name,"value":i.number})
    return JsonResponse(result)


# 添加商品
@login_valid
def add_goods(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        number = request.POST.get("number")
        production = request.POST.get("production")
        safe_date = request.POST.get("safe_date")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")

        goods = Goods()
        goods.name = name
        goods.price = price
        goods.number = number
        goods.production = production
        goods.safe_date = safe_date
        goods.description = description
        goods.picture = picture
        goods.save()
        return HttpResponseRedirect("/Shop/list_goods/")
    return render(request, "shop/add_goods.html")


# 展示商品
@login_valid
def list_goods(request):
    email=request.COOKIES.get("email")
    user=Quser.objects.get(email=email)
    goods_list = user.goods_set.all()
    return render(request, "shop/list_goods.html", locals())


# 用vue+ajax展示商品
from django.views import View
from django.http import JsonResponse
from django.core.paginator import Paginator
from Qshop.settings import PAZE_SIZE


class GoodView(View):
    def get(self, request):
        result = {
            "version": "v1",
            "code": "200",
            "data": [],
            "page_range": [],
            "referer": [],
            "page": []
        }
        id = request.GET.get("id")  # 尝试获取前端get提交的id

        # page=request.GET.get("page")
        # result["page"]=1
        # print(result["page"])
        # if page:
        #     result["page"]=page

        # 如果id存在，获取当前id的数据
        if id:
            goods_data = Goods.objects.get(id=int(id))
            result["data"].append(
                {
                    "id": goods_data.id,
                    "name": goods_data.name,
                    "price": goods_data.price,
                    "number": goods_data.number,
                    "production": goods_data.production,
                    "safe_date": goods_data.safe_date,
                    "description": goods_data.description,
                    "picture": goods_data.picture,
                    "statue": goods_data.statue,
                }
            )
        # 如果id不存在，获取所有数据
        else:
            # 尝试获取页码，如果页码不存在，默认是第一页
            page=request.GET.get("page")
            page_number = request.GET.get("page", 1)
            if page:
                result["page"] = page

            keysords = request.GET.get("keywords")
            # 获取所有数据
            all_goods = Goods.objects.all()
            if keysords:
                all_goods = Goods.objects.filter(name__contains=keysords)
                result["referer"] = "&keywords=%s" % keysords
            # 进行分页
            paginator = Paginator(all_goods, PAZE_SIZE)
            # 获取单页数据
            page_data = paginator.page(page_number)
            # 获取页码
            result["page_range"] = list(paginator.page_range)
            # 对当页数据进行便利，形成字典，可以进行json封装

            goods_data = [{"id": g.id,
                           "name": g.name,
                           "price": g.price,
                           "number": g.number,
                           "production": g.production,
                           "safe_date": g.safe_date,
                           "description": g.description,
                           "picture": g.picture.url,
                           "statue": g.statue, } for g in page_data
                          ]
            result["data"] = goods_data
        return JsonResponse(result)


# vue视图
def vue_list_goods(request):
    id = request.GET.get("id")  # 尝试获取前端get提交的id
    page_data = request.GET.get("page")
    if id:
        goods = Goods.objects.get(id=id)
        if goods.statue == 0:
            goods.statue = 1
        elif goods.statue == 1:
            goods.statue = 0
        goods.save()
    return render(request, "shop/vue_list_goods.html", locals())


# 设置上架和下架
def set_goods(request, id):
    # set_type=request.GET.get("set_type")
    goods = Goods.objects.get(id=int(id))
    if goods.statue == 0:
        goods.statue = 1
    elif goods.statue == 1:
        goods.statue = 0
    goods.save()
    # if set_type=="down":
    #     goods.statue=0
    # elif set_type=="up":
    #     goods.statue=1
    # goods.save()
    return HttpResponseRedirect("/Shop/list_goods/")
    # return HttpResponseRedirect("/Shop/vue_list_goods/")


# 商品详情页
def goods(request, id):
    goods_data = Goods.objects.get(id=int(id))
    return render(request, "shop/goods.html", locals())


# 修改商品信息
def update_goods(request, id):
    goods_data = Goods.objects.get(id=int(id))
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        number = request.POST.get("number")
        production = request.POST.get("production")
        safe_date = request.POST.get("safe_date")
        description = request.POST.get("description")
        picture = request.FILES.get("picture")

        goods_data.name = name
        goods_data.price = price
        goods_data.number = number
        goods_data.production = production.replace("年", "-").replace("月", "-").replace("日", "")
        goods_data.safe_date = safe_date
        goods_data.description = description
        if picture:
            goods_data.picture = picture
        goods_data.save()
        return HttpResponseRedirect("/Shop/goods/%s/" % id)
    return render(request, "shop/update_goods.html", locals())


# 合并测试
def test_goods(request, id=None):
    type_list=GoodsType.objects.all()
    if id:
        goods_data = Goods.objects.get(id=int(id))
    else:
        goods_data = Goods()
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        number = request.POST.get("number")
        production = request.POST.get("production")
        safe_date = request.POST.get("safe_date")
        description = request.POST.get("description")
        goods_type = request.POST.get("goods_type")
        picture = request.FILES.get("picture")

        goods_data.name = name
        goods_data.price = price
        goods_data.number = number
        goods_data.production = production
        goods_data.safe_date = safe_date
        goods_data.description = description
        goods_data.statue = 1
        #把类型整条数据（对象）赋值过去
        goods_data.goods_type = GoodsType.objects.get(id=goods_type)
        #获取cookie当中的店铺
        store_id=request.COOKIES.get("email")
        goods_data.goods_store=Quser.objects.get(email=store_id)

        if picture:
            goods_data.picture = picture
        goods_data.save()
        return HttpResponseRedirect("/Shop/list_goods/")

    return render(request, "shop/test_goods.html", locals())


def base(request):
    return render(request, "shop/base.html")

#订单列表
def order_list(request):
    email=request.COOKIES.get("email")
    user=Quser.objects.get(email=email)
    order_lst=user.order_info_set.all()
    return render(request,"shop/order_list.html",locals())

#发货功能
from Buyer.models import Pay_order
def send_shop(request):
    order_id=request.GET.get("order_id")
    if order_id:
        p_order=Pay_order.objects.get(order_id=order_id)
        p_order.order_state=2
        p_order.save()
    return HttpResponseRedirect("/Shop/order_list/")


from QUser.models import Quser
@login_valid
def profile(request):
    """
    展示个人信息
    :param request:
    :return:
    """
    user_name = request.COOKIES.get("email")
    user = Quser.objects.get(email=user_name)
    if request.method == "POST":
        password = request.POST.get("password")
        user.password = set_password(password)
        user.save()
        response = HttpResponseRedirect("/Shop/login/")
        response.delete_cookie("email")
        response.delete_cookie("user_id")
        request.session.clear()
        return response

    return render(request, "shop/profile.html", {"user": user})


@login_valid
def set_profile(request):
    """
    修改个人信息
    :param request:
    :return:
    """
    user_name = request.COOKIES.get("email")
    user = Quser.objects.get(email=user_name)
    if request.method == "POST":
        user.username = request.POST.get("username")
        user.gender = request.POST.get("gender")
        user.age = request.POST.get("age")
        user.phone = request.POST.get("phone")
        user.address = request.POST.get("address")
        picture = request.FILES.get("picture")
        if picture:
            user.picture = picture
        user.save()
        return HttpResponseRedirect("/Shop/profile/")

    return render(request, "shop/set_profile.html", {"user": user})


def forget_password(request):
    # 后台卖家忘记密码功能
    return render(request, "shop/forgot-password.html")


def reset_password(request):
    """
    重置密码
    1.接收发过来的邮箱，进行校验
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.POST.get("email")
        if email and valid_user(email):
            # 发送邮件内容
            # 首先需要有找回密码页面的地址
            # 其次包含要修改密码的账号
            # 再次包含修改的一个校验码
            # 使用当前时间+账号==》md5加密
            hash_code = set_password(email)
            content = "http://127.0.0.1:8000/Shop/change_password/?email=%s&token=%s" % (email, hash_code)
            # 发送到邮箱
            sendMail(content, email)
    return HttpResponseRedirect("/Shop/forget_password/")


def change_password(request):
    """
    当前人是否有资格修改密码
    :param request:
    :return:
    """
    if request.method == "POST":
        email = request.COOKIES.get("change_email")
        password = request.POST.get("password")
        e = Quser.objects.get(email=email)
        e.password = set_password(password)
        e.save()
        return HttpResponseRedirect("/Shop/login/")

    email = request.GET.get("email")
    token = request.GET.get("token")

    now_token = set_password(email)
    # 当前提交人存在，并且token值正确
    if valid_user(email) and now_token == token:
        respose = render(request, "shop/change_password.html")
        respose.set_cookie("change_email", email)
        return respose
    else:
        return HttpResponseRedirect("/Shop/forget_password/")


# E:\stu\Djangoproject\0805Git\0805Django\Qshop\Shop
from django.http import HttpResponse
from CeleryTask.tasks import add  # , sendMail


def get_celery(request):
    x = 1
    y = 2
    add.delay()
    # sendMail.delay()
    return HttpResponse("调用完成")
