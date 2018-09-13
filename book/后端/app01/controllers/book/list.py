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

    if params.get('book_name'):
        where_dict['name__icontains']=params.get('book_name')
    if params.get('author_name'):
        where_dict['authors__name__icontains'] = params.get('author_name')
    if params.get('publish_name'):
        where_dict['publish__name__icontains'] = params.get('publish_name')
    #基于双下划线的关联查询
    res = Book.objects.filter(**where_dict).values('id','name','price','publish_date','is_valid','authors__id','authors__name','publish__id','publish__name').order_by('-id')[offset1:offset2]
    data={}
    for i in list(res):
        i['authors']=data[i['id']]['authors'] if  data.get(i['id']) else []
        i['authors'].append(i['authors__id'])

        i['author_arr_name'] = data[i['id']]['author_arr_name'] if data.get(i['id']) else []
        i['author_arr_name'].append(i['authors__name'])
        i['authors__name_str']=','.join(i['author_arr_name'])
        data[i['id']]=i
    res_data=[]
    print(connection.queries)
    for index in data:
        res_data.append(data[index])
    return function.ehcoJson({'code':200,'msg':function.ReturnCode[200],'data':res_data,'totalpage':len(res_data)})