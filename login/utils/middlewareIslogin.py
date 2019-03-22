'''
 中间件  判断用户是否登录，这个相当于是一个项目的装饰器，对比自己写的装饰器，粒度更粗。
 同时在中间件处就被拦截，减少继续到 路由->视图函数 这几个块的处理，效率更高

 原理：用户登录入后写session：request.session[settings.USER_SESSION_KEY]='xxxxx'
       在中间件里看是否能取到这个session，取不到，且网页不在白名单则退出到登录界面
'''
import re

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from MakeSomeTools.settings import USER_SESSION_KEY
from django.conf import settings


class Midislogin(MiddlewareMixin):
    def process_request(self, request):
        # 设置带正则表达式的白名单，白名单内的不需要验证，这个在正式项目里可以配置到settings里面
        VALID_PATH_INFO=[ '.*/login/.*','/test/','/rbac/.*','.*/logout/.*','' ]
        current_path=request.path_info

        for valid in  VALID_PATH_INFO: #白名单里的地址不用校验可以直接访问
            reg="^%s$" % (valid)
            print('re.match(',reg,current_path,')=',re.match(reg,current_path))
            if re.match(reg,current_path):
                return None

        else:
            if not request.session.get(settings.USER_SESSION_KEY):
                return redirect("/login/")
            else:
                return None


    def process_response(self, request, response):
        return response


