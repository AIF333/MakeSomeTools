# Create your views here.

from django.shortcuts import render,HttpResponse,redirect
from rbac import models
from rbac.utils.service.init_permission import initPermission



# 登录页面
def login(request):
    if request.method=="GET":
        return render(request,"rbac/login.html")
    else:
        username=request.POST.get("username")
        password=request.POST.get("password")

        # 正式环境密码应该是密文，这里作测试不要求
        user=models.UserInfo.objects.filter(username=username,password=password).first()
        if user:
            # 登录成功 需获取用户的权限信息
            initPermission(request,user)
            return redirect("/rbac/index/")

        else:
            # 登录失败  不做过多处理，只为测试权限系统
            return render(request,"rbac/login.html")

def index(request):
    return render(request,"rbac/index.html")

# 测试用户组
def users(request):
    if request.method=="GET":
        user_list=models.UserInfo.objects.all()

        # print(request,type(request))
        # request.permission_code_list= ['list', 'add', 'del', 'edit', 'list']
        # print(request.permission_code_list) # 用户的权限code
        # return HttpResponse("1111")
        return render(request,"rbac/users.html",{"user_list":user_list,"permission_code_list":request.permission_code_list})
    else:
        pass

# 编辑页面
def users_edit(request,userid):
    return HttpResponse("编辑%s" % userid)

def users_del(request,userid):
    return HttpResponse("删除%s" % userid)



