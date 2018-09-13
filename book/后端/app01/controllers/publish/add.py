from  app01.common import function
from app01.models import *
def index(request):
    params =function.json_decode(request.body)
    data={}
    if not params.get('name'):
        return function.ehcoJson({'code':400,'msg':function.ReturnCode[400]})
    data['name']=params.get('name')
    if not params.get('city'):
        return function.ehcoJson({'code':400,'msg':function.ReturnCode[400]})
    data['city'] = params.get('city')
    if not params.get('email'):
        return function.ehcoJson({'code':400,'msg':function.ReturnCode[400]})
    data['email'] = params.get('email')
    data['is_valid'] = 1

    publish=Publish(**data)
    publish.save()
    if publish:
        print(publish)
        return function.ehcoJson({'code':200,'msg':function.ReturnCode[200]})
    return function.ehcoJson({'code': 500, 'msg': function.ReturnCode[500]})