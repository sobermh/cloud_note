import hashlib

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import User


# Create your views here.


# 注册
def register_view(request):
    # get 返回页面
    if request.method == 'GET':
        return render(request, 'user/register.html')
    # post 处理提交数据
    elif request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        # 1. 两个密码是否一致
        if password1 != password2:
            return HttpResponse('密码不一致')
        # 2. 当前用户是否可用
        old_users = User.objects.filter(username=username)
        if old_users:
            return HttpResponse('用户名已注册')
        # 3. 插入数据

        # 哈希算法 -  给定明文，计算出一段定长的，不可逆的值；md5，sha-256
        # 特点1：定长输出：不管明文输入长度为多少，哈希值都是定长的，md5 -32位16进制
        # 特点2： 不可逆： 无法反向计算出对应的明文
        # 特点3： 雪崩效应： 输入改变，输出必然变
        # 使用场景： 1.密码处理  2.文件的完整新校验
        password_md5 = hashlib.md5(password1.encode()).hexdigest()
        # 有可能报错 -duplicate insert 【唯一索引注意并发写入问题：由于两个相同用户名挤过之前的同一用户名验证导致】
        try:
            user = User.objects.create(username=username, password=password_md5)
        except Exception as e:
            print('%s' % (e))
            return HttpResponse("用户已注册")

        # 存入session免登录一天
        request.session['username'] = username
        request.session['uid'] = user.id
        # 修改session存储时间为1天

        return HttpResponseRedirect('/index')


# 登录
def login_view(request):
    # 获取页面
    if request.method == 'GET':
        #检查登录状态，如果登录了，显示”已登陆“
        if request.session.get('username') and request.session.get('uid'):
            return HttpResponseRedirect('/index/')
        #检查cookies
        c_username = request.COOKIES.get('username')
        c_uid = request.COOKIES.get('uid')
        if c_uid and c_username:
            #回写session
            request.session['username'] = c_username
            request.session['uid'] = c_uid
            return HttpResponseRedirect('/index/')
        return render(request, 'user/login.html')
    # post处理数据
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except Exception as e:
            print(e)
            return HttpResponse('用户名或密码错误')
        # 比对密码
        password_md5 = hashlib.md5(password.encode()).hexdigest()
        if password_md5 != user.password:
            return HttpResponse('用户名或密码错误')
        # 记录会话状态
        request.session['username'] = username
        request.session['uid'] = user.id

        resp = HttpResponseRedirect('/index/')
        # 判断用户是否点选了 ”记住用户名“
        if 'remember' in request.POST:
            resp.set_cookie('username', username, 3600 * 24 * 3)
            resp.set_cookie('uid', user.id, 3600 * 24 * 3)
        return resp


#退出登录
def logout_view(request):
    # 删除session值
    if 'username' in request.session:
        del request.session['username']
    if 'uid' in request.session:
        del request.session['uid']
    #删除Cookies
    resp = HttpResponseRedirect('/index/')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    return resp