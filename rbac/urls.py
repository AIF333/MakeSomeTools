from django.contrib import admin
from django.urls import path, include
from rbac import  views as rb_views

urlpatterns = [
    # 主settings的设置 path('rbac/', include('rbac.urls')),
    path('login/', rb_views.login),  # 登录页面
]