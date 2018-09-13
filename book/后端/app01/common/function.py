from django.shortcuts import render, HttpResponse
import json
#公共方法

ReturnCode={
    200:'操作成功',
    400:'参数错误',
    401:'未登录',
    500:'系统错误'
}

import datetime
from decimal import Decimal

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, Decimal):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)

def ehcoJson(data,content_type='application/json;charset=UTF-8'):
    response = HttpResponse(json.dumps(data,cls=DateEncoder),
                            content_type=content_type)
    return response

def json_decode(str,encoding='utf8'):
    return  json.loads(str, encoding=encoding)

