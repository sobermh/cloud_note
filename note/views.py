import csv

from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from note.models import Note


# Create your views here.


#是否登录的装饰器
def check_login(func):
    def wrap(request, *args, **kwargs):
        if 'username' not in request.session or 'uid' not in request.session:
            c_username = request.COOKIES.get('username')
            c_uid = request.COOKIES.get('uid')
            if not c_uid or c_username:
                return HttpResponseRedirect('/user/login')
            else:
                # 回写session
                request.session['username'] = c_username
                request.session['uid'] = c_uid
        return func(request, *args, **kwargs)
    return wrap


# 添加笔记
@check_login
def add_note(request):
    if request.method == 'GET':
        return render(request, 'note/add_note.html')
    if request.method == 'POST':
        uid = request.session['uid']
        title = request.POST['title']
        content = request.POST['content']
        Note.objects.create(title=title, content=content, user_id=uid)
        return HttpResponse("添加笔记成功")

# 测试分页
def test_page(request):
    #/test_page/4
    #/test_page?page=1
    page_num = request.GET.get('page',1)
    all_date = ['a','b','c','d''e']
    #初始化paginator
    paginator = Paginator(all_date,2)
    # 初始化 具体页码的page对象
    c_page= paginator.page(int(page_num))
    return render(request,'test_page.html',locals())

# 测试csv下载
def test_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment;filename="test.csv"'
    all_data = ['a','b']
    writer = csv.writer(response)
    writer.writerow(all_data)
    return response

