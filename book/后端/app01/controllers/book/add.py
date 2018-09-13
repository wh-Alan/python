from  app01.common import function
from app01.models import *
def index(request):
    params =function.json_decode(request.body)
    data={}
    data2 = {}
    if not params.get('name') or not params.get('price') or not params.get('publish_date') or not params.get('publish__id') or not params.get('authors'):
        return function.ehcoJson({'code':400,'msg':function.ReturnCode[400]})
    data['name']=params.get('name')
    data['price'] = params.get('price')
    data['publish_date'] = params.get('publish_date')
    data['publish_id'] = params.get('publish__id')
    data['is_valid'] = 1

    data2['authors'] = params.get('authors')
    #data2=Author.objects.filter(id__in=params.get('authors'))

    book=Book.objects.create(**data)
    book.authors.add(*data2['authors'])
    if book:
        return function.ehcoJson({'code':200,'msg':function.ReturnCode[200]})
    return function.ehcoJson({'code': 500, 'msg': function.ReturnCode[500]})