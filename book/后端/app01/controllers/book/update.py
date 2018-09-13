from  app01.common import function
from app01.models import *

def index(request):
    params = function.json_decode(request.body)
    if params.get('id') and params.get('name') and params.get('price') and \
            params.get('publish_date') and params.get('publish__id') and params.get('authors') :
        if params.get('is_valid') == 1 or params.get('is_valid') == 0:

            where_dict = {'is_valid': params.get('is_valid')}
            where_dict['name']=params.get('name')
            where_dict['price']=params.get('price')
            where_dict['publish_date']=params.get('publish_date')
            where_dict['publish']=params.get('publish__id')
            #where_dict['authors']=params.get('authors')
            res=Book.objects.filter(id=params.get('id')).update(**where_dict)
            book=Book.objects.filter(id=params.get('id')).first()
            book.authors.set(params.get('authors'))
            if res and book:
                return  function.ehcoJson({'code':200,'msg':function.ReturnCode[200]})
            else:
                return function.ehcoJson({'code': 500, 'msg': function.ReturnCode[500]})
    return function.ehcoJson({'code': 400, 'msg': function.ReturnCode[400]})