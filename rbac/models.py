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
    pid=models.ForeignKey(verbose_name="组内菜单，为空表示为菜单，其他为父级id",
            to='self',null=True,related_name="parent_id",on_delete=models.CASCADE) # related_name反向查询的字段名

    def __str__(self):
        return self.title

class PermissionGroup(models.Model):
    '''权限组表'''
    caption=models.CharField(verbose_name="权限组名称",max_length=64)
    menu=models.ForeignKey(verbose_name="所属的一级菜单",to="Menu",on_delete=models.CASCADE)

    def __str__(self):
        return self.caption

class Menu(models.Model):
    '''一级菜单'''
    menuname=models.CharField(verbose_name="一级菜单名称",max_length=32)


class MyAppUser(object):
    user=models.OneToOneField(to=UserInfo) # 这里就包含了用户名密码
    # other_columns= 这里写其他的字段