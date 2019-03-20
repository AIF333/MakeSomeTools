from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.utils.safestring import mark_safe

from MakeSomeTools.settings import USER_SESSION_KEY
from login import models

# 注册页面
from login.utils.md5 import md5

# 定义一个校验是否登录的装饰器
def is_login(func):
    def inner(request,*args,**kwargs):
        if not request.session.get(USER_SESSION_KEY):
            return redirect("/login/")
        res=func(request,*args,**kwargs)
        return res
    return inner

# 登录页面
def login(request):

    if request.method=="POST":
        username=request.POST.get("username")
        password=md5(request.POST.get("password")) # 密码加密
        print(username,"----",password)

        user=models.User.objects.filter(username=username,password=password)
        if user: # 这里只为测试功能
            request.session[USER_SESSION_KEY]=username
            return redirect("/index/")
        else:
            return redirect("/login/")
        return redirect("/login/")

    return  render(request,"login.html")

# 注销页面
def logout(request):
    if request.session.get(USER_SESSION_KEY):
        del request.session[USER_SESSION_KEY]
    return redirect("/login/")


# 模拟的主页
def index(request):
    username=request.session.get(USER_SESSION_KEY,"")
    print("username=",username,"----",type(username))
    return  render(request,"index.html",{"username":username})


# 模拟的主机管理页面，测试分页功能
def host(request):
    from login.utils.pagination import Pageination

    queryResult=models.ResManage.objects.all()

    pagedict={}
    # request.path_info 可获取当前url的路径，如/host/?page=1的path_url=/host/
    pagedict["url"]=request.path_info
    pagedict["record_sum"]=queryResult.count()
    pagedict["current_page"]=request.GET.get("page")
    pagedict["max_pages"]=11     # 默认11，可不传入
    pagedict["max_records"]=10   # 默认10，可不传入

    page_obj=Pageination(**pagedict)
    res_obj=queryResult[page_obj.start:page_obj.end]

    return render(request,"host.html",{"res_obj":res_obj,"html":page_obj.page()})
