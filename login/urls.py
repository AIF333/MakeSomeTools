from django.contrib import admin
from django.urls import path, include
from login import  views as log_views

urlpatterns = [
    path('login/', log_views.login),  # 登录页面
    path('logout/', log_views.logout),  # 注销页面
    path('', log_views.index),  # 首页
    path('index/', log_views.index),  # 首页
    path('host/', log_views.host),  # 主机管理
    path('test/', log_views.test),  # 主机管理
    path('addHost/', log_views.addHost),  # 主机添加
    path('editHost/<int:resid>', log_views.editHost),  # 主机编辑
    path('delHost/<int:resid>', log_views.delHost),  # 主机删除
]