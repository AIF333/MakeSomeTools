'''
 权限控制的 inclusion_tag ，当用户不同时显示的菜单不同，抽象独立在此
'''

from django import template
from django.conf import settings
register = template.Library()
print("----path:",)
@register.inclusion_tag("rbac/rbac_menu.html") # 默认是在templates路径下
def get_rbac_menu(request):
    menu_dict=request.session.get(settings.USER_MENU_DICT_KEY,None)
    print("menu_dict----",menu_dict)
    return {"menu_dict":menu_dict}

