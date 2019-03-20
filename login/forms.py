from django.forms import Form,fields,widgets
# widgets 插件
class regForm(Form):
    username=fields.CharField(max_length=32,required=True,
        error_messages={"required":"该字段不能为空"})
    password=fields.CharField(max_length=32,required=True,
        widget=widgets.PasswordInput(attrs={"class":"form-control","id":"username","placeholder":"请输入用户名"}))
        # widget 插件增加html的class属性