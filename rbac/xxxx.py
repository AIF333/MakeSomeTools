# d = {'1': {'menu_name': '用户一级菜单',
#            'children': {'1': {'url': '/rbac/users/', 'code': 'list', 'pid': None, 'title': '用户列表', 'acitve': True},
#                         '5': {'url': '/rbac/host/', 'code': 'list', 'pid': None, 'title': '主机列表'},
#                         '6': {'url': '/rbac/host/add/', 'code': 'add', 'pid': None, 'title': '增加主机'},
#                         '7': {'url': '/rbac/host/edit/(\\d+)', 'code': 'edit', 'pid': 5, 'title': '编辑主机'},
#                         '8': {'url': '/rbac/host/del/(\\d+)', 'code': 'del', 'pid': 5, 'title': '删除主机'},
#                         '9': {'url': '/rbac/index/', 'code': 'list', 'pid': 1, 'title': '访问主页', 'active': True}}}}
#
#
#
import re
print(re.match(r'^/rbac/.*$','/rbac/'))
print(re.match(r'^/rbac/.*$','/rbac/a'))
print(re.match(r'^/rbac/.*$','b/rbac/a'))
print(re.match(r'^/rbac/.*$','/arbac/'))
print("-----------------------------")
print(re.match(r'^(?!/rbac/)','/rbac/'))
print(re.match(r'^(?!/rbac/)','/rbac/a'))
print(re.match(r'^(?!/rbac/)','b/rbac/a'))
print(re.match(r'^(?!/rbac/)','/arbac/'))