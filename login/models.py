from django.db import models

# Create your models here.

# 登录页面
class User(models.Model):
    nid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=32,unique=True)
    password=models.CharField(max_length=32)

# 主机管理表
class ResManage(models.Model):
    resid=models.AutoField(primary_key=True)
    resname=models.CharField(max_length=32)
    resip=models.CharField(max_length=32)
