from django.shortcuts import render,HttpResponse
import  json

class BaseControler:
    @classmethod
    def ehcoJson(cls,data):
        response = HttpResponse(json.dumps(data),
                                content_type='application/json;charset=UTF-8')
        return response


