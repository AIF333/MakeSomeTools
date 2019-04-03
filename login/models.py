from django.db import models

# Create your models here.

# 登录页面
class User(models.Model):
    nid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=32,unique=True)
    password=models.CharField(max_length=64) # 密码因为要加密设置大点

    def __str__(self):
        return self.username

# 主机管理表
class ResManage(models.Model):
    resid=models.AutoField(primary_key=True)
    resname=models.CharField(max_length=32)
    resip=models.GenericIPAddressField(protocol="ipv4") # 这种字段只有在modelForm插件才有用
    user=models.ForeignKey(to="User",on_delete=models.CASCADE,default=1)
    dp=models.ManyToManyField(to="Department")

    def __str__(self):
        return self.resname

# 部门表
class Department(models.Model):
    deptid=models.AutoField(primary_key=True)
    deptname=models.CharField(max_length=32)

    def __str__(self):
        return self.deptname

# 测试redis的表，跟其他程序无关
class TestRedis(models.Model):
    key=models.CharField(max_length=32)
    value=models.CharField(max_length=32)