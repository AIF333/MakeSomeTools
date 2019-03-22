import re

from django.conf import settings
def initPermission(request,user):
    '''
        用户登录成功后，权限菜单相关信息的初始化
    :param request: 请求对象
    :param user:登录的用户
    :return: 无返回值，会在session中添加权限和菜单的字典：
        request.session[settings.USER_PERMISSION_KEY] = promission_dict
        request.session[settings.USER_MENU_DICT_KEY] = menu_dict
    '''

    '''
    用户权限信息的初始化：获取用户的权限信息转换成特定格式字典，参数登录的用户
    <QuerySet> ==》字典
    [    {'permissions__url': '/users/', 'permissions__code': 'list', 'permissions__group': 1},
         {'permissions__url': '/host/', 'permissions__code': 'list', 'permissions__group': 2},
         {'permissions__url': '/host/add/', 'permissions__code': 'add', 'permissions__group': 2}, ]
    ====>
    {   1:{'url':['/users/',],'code':['list',]}
        2:{'url':['/host/','/host/add/'],'code':['list','add',]}     }
    '''


    # 过滤掉取消为空的记录，排除某些特殊的角色没有权限对应，为None值的情况
    promission_list = user.roles.filter(permissions__id__isnull=False).values(
        "permissions__id", # 权限id
        "permissions__url", # 带正则的url
        "permissions__code", # 权限code列表
        "permissions__group_id", # 权限组id
        "permissions__group__caption", # 权限组名称
        "permissions__pid",  # 组内菜单id，如果为空说明是菜单，不为空则记录的是同组的菜单id
                              # 如点击 删除按钮需要那个父级菜单有变化（颜色加深...)
        "permissions__group__menu_id",  # 权限组所属的一级菜单id
        "permissions__group__menu__menuname", # 权限组所属的一级菜单名称
        "permissions__title", # 权限名称

         ).distinct()


    #################################################################################
    ##############               菜单的初始化                          ##############
    #################################################################################
    '''
    {'permissions__url': '/rbac/users/', 'permissions__code': 'list', 'permissions__group': 1,
      'permissions__group__caption': '用户权限组', 'permissions__group__menu__menuname': '用户一级菜单',
      'permissions__title': '用户列表', 'permissions__group_menu_id': None}
      '''
    menu_list=[]
    for promission in promission_list:
        var={}
        var['url']=promission['permissions__url'] # 正则url
        var['id']=promission['permissions__id'] # 权限id
        var['code']=promission['permissions__code'] # code码
        # var['group_id']=promission['permissions__group_id'] # 权限组id 暂时无用
        # var['group_caption']=promission['permissions__group__caption'] # 权限组名称，用不到
        var['pid']=promission['permissions__pid'] # 组菜单id，为空则展示，不为空:组的permission_id
        var['menu_id']=promission['permissions__group__menu_id'] # 权限组所属的一级菜单id
        var['menu_name']=promission['permissions__group__menu__menuname'] # 权限组所属的一级菜单名称
        var['title']=promission['permissions__title'] # 权限名称，做二级菜单用
        menu_list.append(var)

    '''
[   {'url': '/rbac/users/', 'id': 1, 'code': 'list', 'pid': None, 'menu_id': 1, 'menu_name': '用户一级菜单', 'title': '用户列表'},
    {'url': '/rbac/host/', 'id': 5, 'code': 'list', 'pid': None, 'menu_id': 1, 'menu_name': '用户一级菜单', 'title': '主机列表'},
    {'url': '/rbac/host/add/', 'id': 6, 'code': 'add', 'pid': None, 'menu_id': 1, 'menu_name': '用户一级菜单','title': '增加主机'},
    {'url': '/rbac/host/edit/(\\d+)', 'id': 7, 'code': 'edit', 'pid': 5, 'menu_id': 1, 'menu_name': '用户一级菜单','title': '编辑主机'},
    {'url': '/rbac/host/del/(\\d+)', 'id': 8, 'code': 'del', 'pid': 5, 'menu_id': 1, 'menu_name': '用户一级菜单', 'title': '删除主机'},
    {'url': '/rbac/index/', 'id': 9, 'code': 'list', 'pid': 1, 'menu_id': 1, 'menu_name': '用户一级菜单', 'title': '访问主页'}     ]  
  转换成：
{1:{
    'menu_name': '用户一级菜单' ,
    children: 	{   1:{'url': '/rbac/users/', 'id': 1, 'code': 'list', 'pid': None, 'title': '用户列表'},	
					5:{'url': '/rbac/host/', 'id': 5, 'code': 'list', 'pid': None, 'title': '主机列表'},	
					6:{'url': '/rbac/host/add/', 'id': 6, 'code': 'add', 'pid': None, 'title': '增加主机'},					
					7:{'url': '/rbac/host/edit/(\\d+)', 'id': 7, 'code': 'edit', 'pid': 5, 'title': '编辑主机'},					
					8:{'url': '/rbac/host/del/(\\d+)', 'id': 8, 'code': 'del', 'pid': 5,  'title': '删除主机'},					
					9:{'url': '/rbac/index/', 'id': 9, 'code': 'list', 'pid': 1, 'title': '访问主页'}   }	
}}
    '''
    # print("---menu_list--",menu_list)
    # 将菜单权限等转换成字典格式，方便快速查找和处理
    menu_dict={}
    for item in menu_list:
        if item['menu_id'] in menu_dict:
            menu_dict[item['menu_id']]['children'][item['id']] = \
                {'url': item['url'], 'code': item['code'], 'pid': item['pid'], 'title': item['title']}
        else:
            menu_dict[item['menu_id']]={
                # 'menu_id':item['menu_id'],
                'menu_name':item['menu_name'],
                'children':{ item['id']:{ 'url':item['url'],'code':item['code'],'pid':item['pid'],'title':item['title']}   },
            }
    # print("menu_dict=",menu_dict)
    '''
 menu_dict = 
 {
    1: {'menu_name': '用户一级菜单',
         'children': {
                  1: {'url': '/rbac/users/', 'code': 'list', 'pid': None, 'title': '用户列表'},
                  5: {'url': '/rbac/host/', 'code': 'list', 'pid': None, 'title': '主机列表'},
                  6: {'url': '/rbac/host/add/', 'code': 'add', 'pid': None, 'title': '增加主机'},
                  7: {'url': '/rbac/host/edit/(\\d+)', 'code': 'edit', 'pid': 5, 'title': '编辑主机'},
                  8: {'url': '/rbac/host/del/(\\d+)', 'code': 'del', 'pid': 5, 'title': '删除主机'},
                  9: {'url': '/rbac/index/', 'code': 'list', 'pid': 1, 'title': '访问主页'}
                       }
        }
}
    '''
    # print('---menu_dict=',menu_dict)
    request.session[settings.USER_MENU_DICT_KEY]=menu_dict





    #################################################################################
    ############                权限的表初始化                          ##############
    #################################################################################
    promission_dict = {}
    for promission in promission_list:
        group = promission['permissions__group_id']
        url = promission['permissions__url']
        code = promission['permissions__code']
        if group in promission_dict:
            promission_dict[group]['url'].append(url)
            promission_dict[group]['code'].append(code)
        else:
            promission_dict[group] = {'url': [url, ], 'code': [code, ]}

    # 写入session
    request.session[settings.USER_PERMISSION_KEY]=promission_dict

    # print(promission_dict)
    # print("-----------------")
    # print(request.session.get(settings.USER_PERMISSION_KEY),"-------")
