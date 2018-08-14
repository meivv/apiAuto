#-*- coding: utf-8 -*-
import sys
# sys.path.append('../apiAtuo/api_auto_test/api_http_request.py')
# sys.path.append('../apiAtuo/api_auto_test/api_read_data_from_excel.py')
# sys.path.append('../apiAtuo/api_auto_test/api_read_data_from_csv.py')
import api_auto_test.api_http_request as http_request
import api_auto_test.api_read_data_from_excel as excl
import configparser
import logging
import logging.config

class test_run(object):

    def __init__(self,conf_file,input_file_name,output_file_name):
        self.conf_file=conf_file
        self.input=input_file_name
        self.output=output_file_name
        conf = configparser.ConfigParser()
        conf.read(self.conf_file)
        section=conf.sections()
        for s in section:
           options=conf.options(s)
           for o in options:
               setattr(self,o,conf.get(s,o))
        if self.case_file_type.lower() == 'excel':
            self.input_file_path = self.data_dir + '/' + self.input + '.xlsx'
            self.input_file = excl.api_rd_wrt_excel(self.input_file_path,'r')

    def __setattr__(self, key, value):
        self.__dict__[key]=value


    def api_run_test_index(self,index):
        work_sheet = self.input_file.excel_get_sheet('接口测试用例')
        basic_data = self.input_file.excel_get_row_value(work_sheet,index)
        for i in range(len(eval(self.case_info))):
            setattr(self, eval(self.case_info)[i], basic_data[i])
        tst_switch=self.on_off
        url=self.protocol+'://'+self.host+self.port+self.path
        header={}
        body={}
        res_save_params = {}
        logging.config.fileConfig('./config/logging.config')
        logger=logging.getLogger('apitestlog')
        # result_dict={}
        if tst_switch=='on':
            if self.header is not None:
                header=eval(self.header)
            if self.body is not None:
                body=eval(self.body)
            request=http_request.api_req_test()
            res=request.api_response(self.method,float(self.timeout),url,header,body).text
            assert_result=True
            if self.res_assertion is not None:
                for value in eval(self.res_assertion):
                    assert_result=assert_result and request.api_res_assertion(res,value)
            if self.res_save_parameter is not None:
                for k,v in eval(self.res_save_parameter).items():
                    value=request.api_save_params(res,v)
                    res_save_params[k]=value
                    setattr(self,k,value)
            result_dict={'result':assert_result,'res_parameter':str(res_save_params),'response':res}
            loginfo='tsResult:'+str(assert_result)+' -- tsURL:'+url+' -- tsHeader:'+str(header)+' -- tsBody:'+str(body)+' -- tsResponse:'+res
            if assert_result==True:
                logger.info(loginfo)
            else:
                logger.error(loginfo)
            return result_dict
        else:
            result_dict={'result':'Off','res_parameter':'','response':''}
            return result_dict

    def api_run_test_batch(self):
        work_sheet = self.input_file.excel_get_sheet('接口测试用例')
        case_num=self.input_file.excel_get_rownum(work_sheet)
        output_file_path = self.result_dir + '/' + self.output + '.xlsx'
        output_file = excl.api_rd_wrt_excel(output_file_path,'w')
        output_sheet_detail=output_file.excel_create_sheet('接口测试结果明细')
        output_sheet_summary=output_file.excel_create_sheet('接口测试结果概况')
        result_header_data = eval(self.case_info)+['test_status','res_parameter','res_text']
        output_file.excel_wrt_row_value(output_sheet_detail,result_header_data)
        for i in range(1,case_num):
            result_dict=self.api_run_test_index(i)
            res_data=[]
            for k in result_dict:
                res_data.append(result_dict[k])
            output_row_data=self.input_file.excel_get_row_value(work_sheet,i)+res_data
            output_file.excel_wrt_row_value(output_sheet_detail,output_row_data)
        case_num=output_file.excel_get_rownum(output_sheet_detail)-1
        api_num=len(list(set(output_file.excel_get_col_value(output_sheet_detail,2))))-1
        case_pass=0
        cass_fail=0
        cass_off=0
        case_pass_rate=0
        for result in output_file.excel_get_col_value(output_sheet_detail,10):
            if str(result).lower()=='true':
                case_pass=case_pass+1
            elif str(result).lower()=='false':
                cass_fail=cass_fail+1
            elif str(result).lower()=='off':
                cass_off=cass_off+1
        if case_num>0:
            case_pass_rate=case_pass/case_num
        summary_data=[['用例总数',case_num],['接口总数',api_num],['用例通过数',case_pass],['用例失败数',cass_fail],['未运行数',cass_off],['用例通过率',case_pass_rate]]
        for row in summary_data:
            output_file.excel_wrt_row_value(output_sheet_summary,row)
        output_file.excel_save()
#
# if __name__ == "__main__":
#     api=test_run('api_cardexchange','api_cardexchange_result')
#     api.api_run_test_batch()
#     print(api.card_jessionId[0])