'''
功能：生成页标的工具类
输入：   :param url: 路由地址，eg：/blog/
        :param record_sum: 记录总数
        :param current_page: 当前查询页
        :param max_pages: 窗口显示的最多页标数，默认11
        :param max_records: 每页的最大记录数，默认10
输出： 安全的页码a标签 eg: <a href ="/resmanage/?page=1">1</a>

eg:
视图函数：
def resutils(request):
    from login.utils.pagination import Pageination

    queryResult=models.ResManage.objects.all()

    pagedict={}
    pagedict["url"]=request.path_info  # request.path_info 可获取当前url的路径，如/resutils/?page=1的path_url=/resutils/
    pagedict["record_sum"]=queryResult.count()
    pagedict["current_page"]=request.GET.get("page")
    pagedict["max_pages"]=15     # 默认11，可不传入
    pagedict["max_records"]=20   # 默认10，可不传入

    page_obj=Pageination(**pagedict)
    res_obj=queryResult[page_obj.start:page_obj.end]

    return render(request,"resmanage.html",{"res_obj":res_obj,"a_html":page_obj.page()})
html:
    <!--页码标签-->
    <style>
        .page a{
            display: inline-block;
            padding: 1px 5px;
            margin: 0px 3px;
            border: 1px solid darkgrey;
            text-align: center;
        }
        .active{
            background-color: cornflowerblue;
        }
    </style>

    <div class="page">{{ a_html }}</div>
'''


from django.utils.safestring import mark_safe

class Pageination(object):

    def __init__(self,url,record_sum,current_page,max_pages=11,max_records=10):
        '''

        :param url: 路由地址，eg：/blog/
        :param record_sum: 记录总数
        :param current_page: 当前查询页
        :param max_pages: 窗口显示的最多页标数，默认11
        :param max_records: 每页的最大记录数，默认10
        '''

        self.url=url
        try:
            self.current_page=int(current_page)
        except Exception:
            self.current_page=1

        self.record_sum=record_sum
        self.max_pages=int(max_pages)
        self.max_records=int(max_records)
        self.page_num, self.last_page_count = divmod(self.record_sum, self.max_records)  # 分页数，最后一页的记录数
        self.half_max_pages=int(self.max_pages/2)

        if self.last_page_count: # 如果最后一页存在记录，则总页数+1
            self.page_num+=1
        if self.current_page> self.page_num or self.current_page<1: # 如果输入的页码不在正常范围，则页码为1
            self.current_page=1

    @property
    def start(self):
        return (self.current_page-1)*self.max_records

    @property
    def end(self):
        return self.current_page*self.max_records

    def page(self):

        if self.page_num <= self.max_pages:
            page_start = 1
            page_end = self.page_num
        else:
            page_start = self.current_page - self.half_max_pages
            page_end = self.current_page + self.half_max_pages + 1

            if page_start <= 1:
                page_start = 1
                page_end = self.max_pages + 1
            if page_end >= self.page_num:
                page_start = self.page_num - self.max_pages
                page_end = self.page_num + 1

        s = []

        s.append('<a href ="%s?page=%s">首页</a>' % (self.url, 1))
        if self.current_page <= 1:
            pre_current_page = self.current_page
        else:
            pre_current_page = self.current_page - 1
        s.append('<a href ="%s?page=%s">上一页</a>' % (self.url, pre_current_page))

        for i in range(page_start, page_end):
            if i == self.current_page:
                s.append('<a href ="%s?page=%s" class="active">%s</a>' % (self.url, i, i))
            else:
                s.append('<a href ="%s?page=%s">%s</a>' % (self.url, i, i))

        if self.current_page == self.page_num:
            nex_current_page = self.page_num
        else:
            nex_current_page = self.current_page + 1

        s.append('<a href ="%s?page=%s">下一页</a>' % (self.url, nex_current_page))
        s.append('<a href ="%s?page=%s">尾页</a>' % (self.url, self.page_num))


        html = "".join(s)

        return  mark_safe(html)

