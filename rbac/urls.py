from django.contrib import admin
from django.urls import path, include
from rbac import  views as rb_views

urlpatterns = [
    # 主settings的设置 path('rbac/', include('rbac.urls')),
    path('login/', rb_views.login),  # 登录页面
    path('index/', rb_views.index),  # 主页面
    path('users/', rb_views.users),  # 用户组页面
    path('users/add/', rb_views.users_add),  # 用户组增加
    path('users/del/<int:userid>', rb_views.users_del),  # 用户组删除
    path('users/edit/<int:userid>', rb_views.users_edit),  # 用户组编辑

    path('host/', rb_views.host),  # 主机组增加
    path('host/add/', rb_views.host_add),  # 主机组增加
    path('host/del/<int:userid>', rb_views.host_del),  # 主机组删除
    path('host/edit/<int:userid>', rb_views.host_edit),  # 主机组编辑
]
