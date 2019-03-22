from django.shortcuts import render,HttpResponse,redirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
import re


class PermissionMiddleware(MiddlewareMixin):
    '''
     session 中的权限字典样式：
     {   1:{'url':['/users/',],'code':['list',]}
        2:{'url':['/host/','/host/add/'],'code':['list','add',]}     }
    '''
    def process_request(self, request):
        # 获取session中的权限字典
        permission_dict=request.session.get(settings.USER_PERMISSION_KEY)
        current_path=request.path_info
        flag=False # 有无权限标志

        # 白名单 不需要验证的链接
        for valid in settings.VALID_URL_LIST :
            if re.match(valid,current_path):
                return None

        # 如果没有获得session，则退出
        if not permission_dict:
            return HttpResponse("未获取到该用户的权限信息")
        else: #获取到权限信息后需与用户的登录路径匹配，如果能匹配上则继续访问，否则退出
            for permission in permission_dict.values():  # {'url':['/users/',],'code':['list',]}
                url_list=permission["url"]
                code_list=permission["code"]
                for rex in url_list:
                    reg=settings.REG_FORMAT %(rex,)  # 这里需要严格匹配
                    # print("---re.match(",reg,current_path)
                    # print("---",re.match(reg,current_path))

                    if re.match(reg,current_path): # 利用正则匹配当前路径和权限表中的正则url路径
                        # 用户有权限  把权限的code传给request
                        flag=True
                        # print("--用户有权限  把权限的code传给request-",code_list)
                        request.permission_code_list=code_list
                        break
                if flag:break
            if not flag:
                return HttpResponse("用户无权访问")

        # 菜单权限获取
        # 增加 active字段 ，即如果当前页是那一页则默认展开，子菜单颜色变化
        menu_flag = False
        current_path = request.path_info
        menu_dict=request.session.get(settings.USER_MENU_DICT_KEY)

        if not menu_dict:
            return HttpResponse("没有获得用户的菜单信息")
        for item in menu_dict.values():
            for url_item in item['children'].values():  # 1: {'url': '/rbac/users/', 'code': 'list', 'pid': None, 'title': '用户列表'
                reg = settings.REG_FORMAT % (url_item['url'],)
                # print("re.match(", reg, current_path, ")=", re.match(reg, current_path))
                if re.match(reg, current_path):  # 如果匹配上，则为父级菜单 和 自己添加属性 active=True
                    active_menu_id = url_item["pid"]
                    if active_menu_id:
                        active_menu_id=str(active_menu_id)   # 取出父级的id 需要转成字符串
                        # print("active_menu_id,str(active_menu_id)", active_menu_id, str(active_menu_id))
                        item['children'][active_menu_id]['acitve'] = True

                    url_item['active'] = True  # 给自己添加属性True
                    menu_flag = True
                    break
                else:  # 未匹配上，不做处理
                    pass
            if menu_flag: # 如果匹配上给一级菜单也加上active
                # print("item['active']=True",item)
                item['active']=True
                break

        request.menu_dict=menu_dict
        print(request.menu_dict)