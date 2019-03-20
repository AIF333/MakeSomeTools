'''
利用md5 进行明文加密，撒盐默认：AIF333

使用，直接传入字符串，返回加密后hash码 ，eg： md5("MyPassWord")
'''

import hashlib
def md5(txt,salt="AIF333"): # 撒盐 默认 salt="AIF333"
    txt=txt+salt
    m=hashlib.md5()
    m.update(txt.encode("utf-8"))
    return m.hexdigest()

