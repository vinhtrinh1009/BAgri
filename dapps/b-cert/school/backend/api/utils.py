import pandas as pd
import numpy as np
import io
import xlrd
from ecies import encrypt, decrypt
from ecies.utils import generate_eth_key
from dotenv import load_dotenv
# from school.models import Student, Professor, Class, Result
# from api.serializers import *

def read_file(file_object):
    excel_df=pd.read_excel(file_object)
    data = excel_df.to_dict(orient='index')
    format_data = {}
    for d_id, d_info in data.items():
        new_d_info = {}
        for key, value in d_info.items():
            new_d_info[key.lower()] = value
        format_data[d_id] = new_d_info
    return format_data

def generate_key_pair():
    private_key = generate_eth_key()
    return private_key

def gen_password(obj):
    
    return

def gen_username(first_name, last_name):

    return

def get_env_token(self):
    
    return

if __name__=='__main__':
    # file = open('/media/dukelee/ntfs/HUST_2017_2022/Thesis/test_utils.xls', 'r')
    raw = read_file('/home/dukelee/Documents/test_data_stud_w_bk_ftu.xlsx')
    for r_id, r_info in raw.items():
        print ("item: ", r_id)
        # for student_id in r_info['student list'].split(','):
        #     student_id = student_id.strip()
        #     print(student_id)
        print(r_info)
    # print(raw)
