"""MakeSomeTools URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from login import  views as log_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', log_views.login),     # 登录页面
    path('logout/', log_views.logout),     # 注销页面
    path('', log_views.index),       #首页
    path('index/', log_views.index), #首页
    path('host/', log_views.host), # 主机管理
    path('test/', log_views.test), # 主机管理
    path('addHost/', log_views.addHost), # 主机添加
    path('editHost/<int:resid>', log_views.editHost), # 主机编辑
    path('delHost/<int:resid>', log_views.delHost), # 主机删除
]
