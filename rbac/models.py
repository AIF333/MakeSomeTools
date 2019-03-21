from django.db import models

# Create your models here.
class UserInfo(models.Model):
    '''用户表'''
    username=models.CharField(verbose_name="用户名称",max_length=32)
    password=models.CharField(verbose_name="用户密码",max_length=64)
    roles=models.ManyToManyField(verbose_name="用户拥有的角色",to="Role")

    def __str__(self):
        return self.username

class Role(models.Model):
    '''角色表'''
    title=models.CharField(verbose_name="角色名称",max_length=64)
    permissions=models.ManyToManyField(verbose_name="角色拥有的权限",to="Permission")

    def __str__(self):
        return self.title

class Permission(models.Model):
    '''权限表'''
    title=models.CharField(verbose_name="权限名称",max_length=64)
    url=models.CharField(verbose_name="含有正则的url",max_length=255)
    code=models.CharField(verbose_name="权限代码",max_length=32)
    group=models.ForeignKey(verbose_name="所属权限组",to="PermissionGroup",on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class PermissionGroup(models.Model):
    caption=models.CharField(verbose_name="权限组名称",max_length=64)

    def __str__(self):
        return self.caption


