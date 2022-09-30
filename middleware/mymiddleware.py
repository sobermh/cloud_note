"""
@author:maohui
@time:9/30/2022 8:46 AM
  　　　　　　　 ┏┓    ┏┓+ +
  　　　　　　　┏┛┻━━━━┛┻┓ + +
  　　　　　　　┃        ┃ 　 
  　　　　　　　┃     ━  ┃ ++ + + +
  　　　　　 　████━████ ┃+
  　　　　　　　┃        ┃ +
  　　　　　　　┃   ┻    ┃
  　　　　　　　┃        ┃ + +
  　　　　　　　┗━┓   ┏━━┛
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃ + + + +
  　　　　　　　  ┃   ┃　　　Code is far away from bug with the animal protecting
  　　　　　　　  ┃   ┃+ 　　　　神兽保佑,代码无bug
  　　　　　　　  ┃   ┃
  　　　　　　　  ┃   ┃　　+
  　　　　　　　  ┃   ┗━━━━━━━┓ + +     
  　　　　　　　  ┃           ┣┓
  　　　　　　　  ┃           ┏┛
  　　　　　　　  ┗┓┓┏━━━━━┳┓┏┛ + + + +
  　　　　　　　   ┃┫┫     ┃┫┫
  　　　　　　　   ┗┻┛     ┗┻┛+ + + +
"""
import re
import traceback

from django.core import mail
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

#test
class MyMiddleware(MiddlewareMixin):
    def process_request(self, request):
        print("mymiddleware process_request do-----")

    def process_view(self, request, callback, callback_args, callback_kwargs):
        print("mymiddleware process_view do-----")

    def process_response(self, request, response):
        print("mymiddleware process_reposne do-----")
        return response

#限制浏览次数
class VisitLimit(MiddlewareMixin):

    visit_times={}
    def process_request(self,request):
        ip_address = request.META['REMOTE_ADDR']
        path_url = request.path_info
        if not re.match('^/test',path_url):
            return None
        times =self.visit_times.get(ip_address,0)
        print('ip',ip_address,'已经访问',times)
        self.visit_times[ip_address] =times+1
        if times < 5:
            return None
        return HttpResponse("访问被禁止")


#异常发送邮箱
# class ExceptionMiddleWare(MiddlewareMixin):
#
#     def process_exception(self,request,exception):
#         print(exception)
#         print(traceback.format_exc())
#
#         mail.send_mail(subject="cloud_note出错了",message=traceback.format_exc(),from_email='409788696@qq.com',recipient_list=settings.EX_EMAIL)
#         return HttpResponse("访问有误")