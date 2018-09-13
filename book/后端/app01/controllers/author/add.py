from  app01.common import function
from app01.models import *
def index(request):
    params =function.json_decode(request.body)
    data={}
    data2 = {}
    if not params.get('name') or not params.get('age') or not params.get('phone') or not params.get('birthday') or not params.get('addr'):
        return function.ehcoJson({'code':400,'msg':function.ReturnCode[400]})
    data['name']=params.get('name')
    data['age'] = params.get('age')
    data['is_valid'] = 1

    data2['phone'] = params.get('phone')
    data2['birthday'] = params.get('birthday')
    data2['addr'] = params.get('addr')
    authorDetail=AuthorDetail.objects.create(**data2)
    author=Author(**data,author_detail=authorDetail)
    author.save()
    if author:
        print(author)
        return function.ehcoJson({'code':200,'msg':function.ReturnCode[200]})
    return function.ehcoJson({'code': 500, 'msg': function.ReturnCode[500]})