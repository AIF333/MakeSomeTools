from django.db import models
from django.forms.models import ModelForm
from django.test import TestCase

# 生成主机表的测试数据
# from login import models
#
# for i in range(1,201):
#     resname="主机%s号" % (i,)
#     resip="100.%s.196.%s" % (i,i)
#     dic={"resname":resname,"resip":resip}
#     models.ResManage.objects.create(**dic)

# print(divmod(91,10))


import hashlib
def md5(txt,salt="AIF333"): # 撒盐 默认 salt="AIF333"
    txt=txt+salt
    m=hashlib.md5()
    m.update(txt.encode("utf-8"))
    return m.hexdigest()


a="yeteng123"

print(md5(a))

