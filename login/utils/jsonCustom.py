'''
 json 格式的自定义，在序列化有datetime或date类型时可支持序列化

 使用参考：
     from login.utils.jsonCustom import JsonCustomEncoder
    import datetime

     dic={"k1":"v1","datetime": datetime.datetime.now()}
    print(json.dumps(dic,cls=JsonCustomEncoder))
'''

import datetime
import json


class JsonCustomEncoder(json.JSONEncoder):

    def default(self, field):

        if isinstance(field, datetime.datetime):
            return field.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(field, datetime.date):
            return field.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, field)