import datetime
import json

from django.core import serializers
from django.shortcuts import render,HttpResponse,redirect

# Create your views here.
from django.utils.safestring import mark_safe

# from MakeSomeTools import  settings # 只会导入看到的
from django.conf import settings # 会导入所有的配置
from login import models

# 注册页面
from login.forms import regForm, ResModelForm
from login.utils.jsonCustom import JsonCustomEncoder
from login.utils.md5 import md5

# 定义一个校验是否登录的装饰器
def is_login(func):
    def inner(request,*args,**kwargs):
        if not request.session.get(settings.USER_SESSION_KEY):
            return redirect("/login/")
        res=func(request,*args,**kwargs)
        return res
    return inner

# 登录页面
def login(request):

    # if request.method=="POST":
        # username=request.POST.get("username")
        # password=md5(request.POST.get("password")) # 密码加密
        # print(username,"----",password)
        #
        # user=models.User.objects.filter(username=username,password=password)
        # if user: # 这里只为测试功能
        #     request.session[settings.USER_SESSION_KEY]=username
        #     return redirect("/index/")
        # else:
        #     return redirect("/login/")
        # return redirect("/login/")

        # 使用form组件
    if request.method=="GET":
        regform = regForm()
        return render(request, "login/login.html", {"regform":regform})
    else:
        regform=regForm(request.POST)

        if regform.is_valid():
            username=regform.cleaned_data.get("username")
            password=regform.cleaned_data.get("password")
            if models.User.objects.filter(username=username,password=md5(password)):
                print("%s用户登录成功" % (username,))
                request.session[settings.USER_SESSION_KEY]=username
                return redirect("/index/")
            else:
                regform.add_error("password", "用户名或密码错误")
                return render(request, "login/login.html", {"regform": regform})
        else:
            print("校验不通过")
            return HttpResponse("校验不通过")

                # return  render(request,"login.html")

# 注销页面
def logout(request):
    if request.session.get(settings.USER_SESSION_KEY):
        del request.session[settings.USER_SESSION_KEY]
    return redirect("/login/")


# 模拟的主页
def index(request):
    username=request.session.get(settings.USER_SESSION_KEY,"")
    print("username=",username,"----",type(username))
    return  render(request, "login/index.html", {"username":username})


# 模拟的主机管理页面，测试分页功能
def host(request):
    if request.method=="GET":
        from login.utils.pagination import Pageination

        queryResult=models.ResManage.objects.order_by("-resid").all()

        pagedict={}
        # request.path_info 可获取当前url的路径，如/host/?page=1的path_url=/host/
        pagedict["url"]=request.path_info
        pagedict["record_sum"]=queryResult.count()
        pagedict["current_page"]=request.GET.get("page")
        pagedict["max_pages"]=11     # 默认11，可不传入
        pagedict["max_records"]=10   # 默认10，可不传入

        page_obj=Pageination(**pagedict)
        print("---",page_obj)
        res_obj=queryResult[page_obj.start:page_obj.end]

        return render(request, "login/host.html", {"res_obj":res_obj, "html":page_obj.page()})
    else:
        pass

# 添加主机
def addHost(request):
    if request.method=="GET":
        resForm=ResModelForm()
        return render(request, "login/addHost.html", {"resForm":resForm})
    else:
        resForm = ResModelForm(request.POST)
        if resForm.is_valid():
            resForm.save()
        return redirect("/host/")

# 编辑主机
def editHost(request,resid):
    # 获取编辑的主机id
    resobj = models.ResManage.objects.filter(resid=int(resid)).first()
    if not resobj:
        return redirect("/host/")
    print("---", resid, resobj)


    if request.method=="GET":
        resForm=ResModelForm(instance=resobj) # 编辑时用 instance
        print("---",resForm)
        return render(request, "login/editHost.html", {"resForm":resForm})
    else:
        resForm=ResModelForm(data=request.POST,instance=resobj)
        if resForm.is_valid():
            resForm.save()
            return redirect("/host/")
        else:
            return render(request, "login/editHost.html", {"resForm": resForm})

# 删除主机
def delHost(request,resid):
    res=models.ResManage.objects.filter(resid=int(resid))
    resobj=res.first()
    if not resobj:
        return redirect("/host/")

    if request.method=="GET":
        resForm=ResModelForm(instance=resobj)
        return render(request, "login/delHost.html", {"resForm":resForm})
    else:
        resdel=res.delete()  # 删除时会manytomany关联也删除
        print("--resdel-",resdel)
        return redirect("/host/")

# 测试页面
def test(request):
    host_list=models.ResManage.objects.filter(resid__lt=3)
    host_list_values=models.ResManage.objects.filter(resid__lt=3).values()
    print("---host_list:",host_list,"---type(host_list):",type(host_list))
    print("---host_list_values:",host_list_values,"---type(host_list_values):",type(host_list_values))

    # 具体的记录 可以直接将 queryset 使用list方法后序列化
    print('---json.dumps(list(host_list)):',json.dumps(list(host_list_values)))

    # 对象则需使用django的模块
    host_ser=serializers.serialize("json",host_list)
    print('---host_ser:',type(host_ser),host_ser)

    from login.utils.jsonCustom import JsonCustomEncoder

    dic={"k1":"v1","datetime": datetime.datetime.now()}
    print(json.dumps(dic,cls=JsonCustomEncoder))

    return render(request, "login/test.html")