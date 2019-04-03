from django.contrib import admin
from django.urls import path, include
from login import  views as log_views

urlpatterns = [
    path('login/', log_views.login),  # 登录页面
    path('logout/', log_views.logout),  # 注销页面
    path('', log_views.index),  # 首页
    path('index/', log_views.index),  # 首页
    path('host/', log_views.host),  # 主机管理
    path('addHost/', log_views.addHost),  # 主机添加
    path('editHost/<int:resid>', log_views.editHost),  # 主机编辑
    path('delHost/<int:resid>', log_views.delHost),  # 主机删除
    path('test/', log_views.test),  # 测试
    path('test1/', log_views.test_db2redis),  # 测试数据库数据导入到redis中
    path('test2/', log_views.test_redis2db),  # 测试redis数据导入到db中
]