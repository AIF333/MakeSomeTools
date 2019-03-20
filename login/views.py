from django.shortcuts import render,HttpResponse

# Create your views here.
from django.utils.safestring import mark_safe

from login import models


def resmanage(request):
    queryResult=models.ResManage.objects.all()
    if request.GET.get("page"):
        current_page = int(request.GET.get("page"))
    else:
        current_page = 1

    # max_records 每页最大显示记录数  current_page 当前页 总记录数
    max_records=10
    record_sum=queryResult.count()
    page_num,last_page_count=divmod(record_sum,max_records) # 分页数，最后一页的记录数
    max_pages=11  # 最大的页标数
    half_max_pages=int(max_pages/2)

    if last_page_count: # 如果最后一页有记录，则页数加1
        page_num+=1

    if page_num <= max_pages:
        page_start=1
        page_end=page_num
    else:
        page_start=current_page-half_max_pages
        page_end=current_page+half_max_pages+1

        if page_start<=1:
            page_start=1
            page_end=max_pages+1
        if page_end>=page_num:
            page_start=page_num-max_pages
            page_end=page_num+1


    s=[]

    if current_page <=1 :
        pre_current_page=current_page
    else:
        pre_current_page = current_page-1
    s.append('<a href ="%s?page=%s">上一页</a>' % ("/resmanage/",pre_current_page))

    for i in range(page_start,page_end):
        if i == current_page:
            s.append('<a href ="%s?page=%s" class="active">%s</a>' % ("/resmanage/",i,i))
        else:
            s.append('<a href ="%s?page=%s">%s</a>' % ("/resmanage/",i,i))

    if current_page == page_num:
        nex_current_page=page_num
    else:
        nex_current_page=current_page+1

    s.append('<a href ="%s?page=%s">下一页</a>' % ("/resmanage/",nex_current_page))

    html="".join(s)

    start=(current_page-1)*max_records
    end=current_page*max_records

    res_obj=models.ResManage.objects.all()[start:end]
    return render(request,"resmanage.html",{"res_obj":res_obj,"a_html":mark_safe(html)})

def resutils(request):
    from login.utils.pagination import Pageination

    queryResult=models.ResManage.objects.all()

    pagedict={}
    pagedict["url"]=request.path_info
    pagedict["record_sum"]=queryResult.count()
    pagedict["current_page"]=request.GET.get("page")
    pagedict["max_pages"]=15     # 默认11，可不传入
    pagedict["max_records"]=20   # 默认10，可不传入

    page_obj=Pageination(**pagedict)
    res_obj=queryResult[page_obj.start:page_obj.end]

    return render(request,"resmanage.html",{"res_obj":res_obj,"a_html":page_obj.page()})