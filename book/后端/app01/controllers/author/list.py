from  app01.common import function
from app01.models import *
from django.db import connection
def index(request):
    params = function.json_decode(request.body)
    page=params.get('page') if params.get('page') else 1
    limit = params.get('limit') if params.get('limit') else 10
    offset1=(page-1)*limit
    offset2=page*limit
    if params.get('is_valid')==1 or params.get('is_valid')==0:
        where_dict={'is_valid':params.get('is_valid')}
    else:
        where_dict={}
    if params.get('name'):
        where_dict['name__icontains']=params.get('name')
    if params.get('phone') and params.get('phone').isdigit():
        where_dict['author_detail__phone'] = int(params.get('phone'))
    #基于双下划线的关联查询
    res = Author.objects.filter(**where_dict).values('id','name','age','is_valid','author_detail__phone','author_detail__birthday','author_detail__addr').order_by('-id')[offset1:offset2]
    data=[]
    for i in res:
        i['phone']=i['author_detail__phone']
        i['birthday']=i['author_detail__birthday']
        i['addr']=i['author_detail__addr']
        data.append(i)
    return function.ehcoJson({'code':200,'msg':function.ReturnCode[200],'data':data,'totalpage':len(data)})