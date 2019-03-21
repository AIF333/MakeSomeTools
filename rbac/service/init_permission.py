from django.conf import settings


def initPermission(request,user):
    '''
        用户登录成功后，权限相关信息的初始化
    :param request: 请求对象
    :param user:登录的用户
    :return: 无返回值，会在session中添加权限的字典
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

    promission_list = user.roles.values("permissions__url", "permissions__code", "permissions__group").distinct()
    promission_dict = {}

    for promission in promission_list:
        group = promission['permissions__group']
        url = promission['permissions__url']
        code = promission['permissions__code']
        if group in promission_dict:
            promission_dict[group]['url'].append(url)
            promission_dict[group]['code'].append(code)
        else:
            promission_dict[group] = {'url': [url, ], 'code': [code, ]}

    # 写入session
    request.session[settings.USER_PERMISSION_KEY]=promission_dict
    print(promission_dict)
    print("-----------------")
    print(request.session.get(settings.USER_PERMISSION_KEY),"-------")
