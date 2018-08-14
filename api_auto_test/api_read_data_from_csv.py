#-*- coding: utf-8 -*-
import csv
class api_rd_wrt_csv(object):

    def __init__(self,csv_path):
        try:
            with open(csv_path,'r') as self.csv:
                self.csv_reader=csv.reader(self.csv,delimiter=',')
                self.csv_header=next(self.csv_reader)
                self.csv_reader_dict=csv.reader(self.csv,self.csv_header,delimiter=',')
                # self.csv_writer=csv.writer(self.csv,delimiter=',')
        except Exception as e:
            print(e)

    #按照列号获取CSV某行值
    def csv_get_value_by_row(self,row_index):
        try:
            return self.csv_reader[row_index]
        except Exception as e:
            print(e)
            return None

    #按照列名和行号获取某单元格值
    def csv_get_value_by_dict(self,col_name,row_index):
        try:
            return self.csv_reader_dict[col_name][row_index]
        except Exception as e:
            print(e)
            return None
    #
    # #在CSV中写入新行
    # def csv_wrt_by_row(self,*row):
    #     try:
    #         self.csv_writer.writerow(row)
    #     except Exception as e:
    #         print(e)

    #关闭CSV文件
    def csv_close(self):
        try:
            self.csv.close()
        except Exception as e:
            print(e)

