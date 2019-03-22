from django.forms import Form, fields, ModelForm,widgets
 # 因为和modelForm插件下的widget重名，所以起个别名

# widgets 插件
from login import models


class regForm(Form):
    username=fields.CharField(max_length=32,required=True,
        error_messages={"required":"该字段不能为空"},
                              label="用户名")
    password=fields.CharField(max_length=32,required=True,label="密码",
        widget=widgets.PasswordInput(attrs={"class":"form-control","id":"username","placeholder":"请输入密码"}))
        # widget 插件增加html的class属性

from django.forms import widgets as wid
class ResModelForm(ModelForm):
    class Meta:
        model = models.ResManage  # 对应的Model中的类
        fields = "__all__"  # 字段，如果是__all__,就是表示列出所有的字段,列表形式
        exclude = None  # 排除的字段
        labels={"resname": "主机名", "resip": "IP"} # 提示信息
        help_texts = None  # 帮助提示信息
        widgets = {
            "resname": wid.Textarea(attrs={"class": "c1"})  # 还可以自定义属性 # 自定义插件
        }         # widgets用法,比如把输入用户名的input框给为Textarea
        error_messages = None  # 自定义错误信息
        # error_messages用法：
        error_messages = {
            'resname': {'required': "主机名不能为空", },
            'resip': {'required': "IP不能为空", },
        }



# labels，自定义在前端显示的名字