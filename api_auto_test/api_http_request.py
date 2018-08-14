#-*- coding: utf-8 -*-
import requests
import json
import re
class api_req_test(object):
    def __init__(self):
        pass

    #获取HTTP请求的返回
    def api_response(self,method,time_out,url,header,param):
        if method.lower()=='post':
            resp=requests.post(url,timeout=time_out,headers=header,data=json.dumps(param))
        elif method.lower()=='get':
            resp=requests.get(url,timeout=time_out,headers=header,params=param)
        else:
            # print(header)
            resp=None
        return resp

    #通过返回值校验HTTP请求是否成功
    def api_res_assertion(self,resp,value):
        if value in resp:
            return True
        else:
            return False

    #通过正则表达式，获取HTTP返回的对应内容
    def api_save_params(self,resp,reg_exp):
        try:
            return re.findall(reg_exp,resp)
        except Exception as e:
            print(e)
            return None

