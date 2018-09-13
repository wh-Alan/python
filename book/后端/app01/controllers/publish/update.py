from  app01.common import function
from app01.models import *

def index(request):
    params = function.json_decode(request.body)
    if params.get('id') and params.get('name') and params.get('email') and params.get('city'):
        if params.get('is_valid') == 1 or params.get('is_valid') == 0:

            where_dict = {'is_valid': params.get('is_valid')}
            where_dict['name']=params.get('name')
            where_dict['email']=params.get('email')
            where_dict['city']=params.get('city')
            res=Publish.objects.filter(id=params.get('id')).update(**where_dict)
            if res :
                return  function.ehcoJson({'code':200,'msg':function.ReturnCode[200]})
            else:
                return function.ehcoJson({'code': 500, 'msg': function.ReturnCode[500]})
    return function.ehcoJson({'code': 400, 'msg': function.ReturnCode[400]})