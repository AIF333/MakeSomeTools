# Create your views here.

from django.shortcuts import render,HttpResponse,redirect
from rbac import models
from rbac.service.init_permission import initPermission



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
            return HttpResponse("登录成功")

        else:
            # 登录失败  不做过多处理，只为测试权限系统
            return render(request,"rbac/login.html")




