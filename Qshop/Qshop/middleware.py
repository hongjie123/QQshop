from django.utils.deprecation import MiddlewareMixin #所有中间件的复件
from django.http import HttpResponse

class MiddleWareIp(MiddlewareMixin):
    def process_request(self,request):
        request_ip=request.META["REMOTE_ADDR"]
        if request_ip=="127.0.0.2":
            return HttpResponse("中间件，request请求之前，禁止此IP访问。")

    def process_view(self,request,callback,callback_args,callback_keywords):
        """
        :param request: 请求
        :param callback:  视图函数，请求哪个视图，就是哪个视图函数
        :param acllback_args: 视图函数需要的参数  元组类型
        :param callback_keywords: 视图函数粗腰的参数  字典类型
        :return:
        """
        print(callback)

    def process_exception(self,request,exception):
        print(exception)
        import os
        import datetime
        from Qshop.settings import BASE_DIR
        log_path=os.path.join(BASE_DIR,"error.log")
        with open(log_path,"a") as f:
            now=datetime.datetime.now().strftime("%Y-%M-%D %H:%M:%S")
            content="[%s]:%s\n"%(now,str(exception))
            f.write(content)
        print("我是process_exception")
    def process_template_response(self,request,response):
        """
        :param request: 请求
        :param response: 视图的响应
        :return:
        """
        print("我是process_template_response")
        return response

    def process_response(self,request,response):
        for method in dir(response):
            if not method.startswith("_"):
                print(method)
        # print(dir(response))
        response.set_cookie("hello","world")
        return response

