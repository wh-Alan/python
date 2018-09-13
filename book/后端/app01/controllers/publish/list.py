from  app01.common import function
from app01.models import *

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
    res = Publish.objects.filter(**where_dict).order_by('-id')[offset1:offset2]
    data=[]
    i=0;
    for li in res:
        data.append({
            'id':li.id,
            'name':li.name,
            'email':li.email,
            'city':li.city,
            'is_valid':li.is_valid
        })
        i+=1
    return function.ehcoJson({'code':200,'msg':function.ReturnCode[200],'data':data,'totalpage':i})