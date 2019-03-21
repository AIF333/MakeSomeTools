from django.contrib import admin
from django.urls import path, include
from rbac import  views as rb_views

urlpatterns = [
    # 主settings的设置 path('rbac/', include('rbac.urls')),
    path('login/', rb_views.login),  # 登录页面
    path('index/', rb_views.index),  # 主页面
    path('users/', rb_views.users),  # 主机组页面
    path('users/edit/<int:userid>', rb_views.users_edit),  # 主机组页面
    path('users/del/<int:userid>', rb_views.users_del),  # 主机组页面
]
