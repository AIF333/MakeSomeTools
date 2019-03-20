'''
 中间件  判断用户是否登录，这个相当于是一个项目的装饰器，对比自己写的装饰器，粒度更粗。
 同时在中间件处就被拦截，减少继续到 路由->视图函数 这几个块的处理，效率更高
'''

from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from MakeSomeTools.settings import USER_SESSION_KEY


class Midislogin(MiddlewareMixin):
    def process_request(self, request):
        if request.path_info  == "/login/":
            return None
        else:
            if not request.session.get(USER_SESSION_KEY):
                return redirect("/login/")
            else:
                return None


    def process_response(self, request, response):
        return response


