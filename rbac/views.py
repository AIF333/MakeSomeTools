# Create your views here.

from django.shortcuts import render,HttpResponse,redirect
from rbac import models
from rbac.utils.service.init_permission import initPermission



# 登录页面
def login(request):
    if request.method=="GET":
        return render(request, "rbac/login.html")
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
            return render(request, "rbac/login.html")


def logout(request):
    from django.conf import  settings
    session_list=[settings.USER_PERMISSION_KEY,settings.USER_PERMISSION_KEY]
    for sei in session_list:
        print("request.session.get(sei,False)",request.session.get(sei,False))
        if request.session.get(sei,False):
            del request.session[sei]

    return redirect('/rbac/login/')


# 主页面
def index(request):
    return render(request,"rbac/index.html")

# 测试用户组
def users(request):
    if request.method=="GET":
        user_list=models.UserInfo.objects.all()
        return render(request,"rbac/users.html",
                      {"user_list":user_list})
    else:
        pass

# 编辑页面
def users_edit(request,userid):
    return HttpResponse("编辑%s" % userid)

def users_del(request,userid):
    return HttpResponse("删除%s" % userid)

def users_add(request):
    return HttpResponse("增加")
# 主机组
def host(request):
    from login import  models as l_models
    if request.method=="GET":
        from login.utils.pagination import Pageination

        queryResult=l_models.ResManage.objects.order_by("-resid").all()

        pagedict={}
        # request.path_info 可获取当前url的路径，如/host/?page=1的path_url=/host/
        pagedict["url"]=request.path_info
        pagedict["request"]=request
        pagedict["record_sum"]=queryResult.count()
        pagedict["current_page"]=request.GET.get("page")
        pagedict["max_pages"]=11     # 默认11，可不传入
        pagedict["max_records"]=10   # 默认10，可不传入

        page_obj=Pageination(**pagedict)
        print("---",page_obj)
        res_obj=queryResult[page_obj.start:page_obj.end]

        return render(request, "rbac/host.html",
            {"res_obj":res_obj, "html":page_obj.page() })
    else:
        pass

# 编辑页面
def host_edit(request,userid):
    return HttpResponse("编辑%s" % userid)

def host_del(request,userid):
    return HttpResponse("删除%s" % userid)

def host_add(request):
    return HttpResponse("增加")
