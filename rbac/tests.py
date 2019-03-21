from django.test import TestCase

# Create your tests here.

# d1={"k1":"v1","k2":"v2","k3":"v3"}
# #
# # for d in d1.values():
# #     print(d)

import re


print(re.match(r'/rbac/(users|host)/$',"/rbac/users/a"))