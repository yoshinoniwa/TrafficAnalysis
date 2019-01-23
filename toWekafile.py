import csv
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import numpy as np
import math
import scipy.stats
import re
from statistics import mean, variance, stdev
from scipy.io import arff
from tornado.netutil import add_accept_handler
from xlwings.constants import FilterAllDatesInPeriod
from astropy.units import darad
from scipy.cluster.hierarchy import set_link_color_palette
from matplotlib.rcsetup import all_backends
from _tkinter import create
# from bitarray._bitarray import length

# グローバル変数
day = "2016-10-06"
file_name = "data_by_ipaddress/weka/"+day+".csv"
all_data_list = list()
data_format_list = list()

ipaddress_list = list()


def comparisionIP(ip):
    file_name_list = ip.tolist()#リスト型へ変換
    lst = list()
    for f in file_name_list:
        to_str = str(f)
        if '_1' in to_str:
            ip_str = re.sub(r'_1|\[|\'|\]', "", to_str)
        lst.append(ip_str)
#         print(ip_str)
    ipaddress_list = list(set(lst))
    return ipaddress_list

#ipアドレスごとにデータをセット
def dataSet(d_lst,ip_lst):
    data_list = d_lst
    all_list = list()
    for ip in ip_lst:
        set_list = list()
        count =0
        for d in data_list:
            ipad = str(d[4])
            if ip in ipad:
                set_list.append(d)
                count +=1
        all_list.append(set_list) 
    return all_list 
    
def dataFormatSet(lst):
    count = 0
    d_f_list = list()
    ip_lst = list()
    for l in lst:
        to_str = str(l)
#         print(len(l))
        to_cut = re.sub('\[|\]|\'', "", to_str)
        ip = str(l[0][4])
        set_value = ''
#         print(l)
        cluster_num = len(l) #クラスタ数
        a_d = ['time_aveg1','time_sd1','data_aveg1','data_sd1','time_aveg2','time_sd2','data_aveg2','data_sd2','cluster']
        
        if cluster_num == 1:
            a_d[0] = l[0][0]
            a_d[1] = l[0][1]
            a_d[2] = l[0][2]
            a_d[3] = l[0][3]
            a_d[4] = 0
            a_d[5] = 0
            a_d[6] = 0
            a_d[7] = 0
            a_d[8] = cluster_num
            d_f_list.append(a_d)
            ip_lst.append(str(l[0][4]))
#             print(set_valued)
        if cluster_num == 2:
            ip2 = str(l[1][4])
            a_d[0] = l[0][0]
            a_d[1] = l[0][1]
            a_d[2] = l[0][2]
            a_d[3] = l[0][3]
            a_d[4] = l[1][0]
            a_d[5] = l[1][1]
            a_d[6] = l[1][2]
            a_d[7] = l[1][3]
            a_d[8] = cluster_num
            d_f_list.append(a_d)
            ip_lst.append(str(l[0][4]))
        if cluster_num == 3:
            l3 = sorted(l, key=lambda student: student[2],reverse=True)
            a_d[0] = l3[0][0]
            a_d[1] = l3[0][1]
            a_d[2] = l3[0][2]
            a_d[3] = l3[0][3]
            a_d[4] = l3[1][0]
            a_d[5] = l3[1][1]
            a_d[6] = l3[1][2]
            a_d[7] = l3[1][3]
            a_d[8] = cluster_num
            d_f_list.append(a_d)
            ip_lst.append(str(l[2][4]))
        if cluster_num == 4:
            l4 = sorted(l, key=lambda student: student[2],reverse=True)
            a_d[0] = l4[0][0]
            a_d[1] = l4[0][1]
            a_d[2] = l4[0][2]
            a_d[3] = l4[0][3]
            a_d[4] = l4[1][0]
            a_d[5] = l4[1][1]
            a_d[6] = l4[1][2]
            a_d[7] = l4[1][3]
            a_d[8] = cluster_num
            d_f_list.append(a_d)
            ip_lst.append(str(l[3][4]))
        if cluster_num == 5:
            ip2 = str(l[1][4])
            ip3 = str(l[2][4])
            ip4 = str(l[3][4])
            ip5 = str(l[4][4])
        count +=1
    print(ip_lst)
    createDatabyIPaddressFile(ip_lst)
    return d_f_list

def createCSVFile(l):
    f_name = 'data_by_ipaddress/weka/'+day+'_input' + '.csv'
    f = open(f_name, 'w')
    title_name = ['time_ave1','time_sd1','data_ave1','data_sd1','time_ave2','time_sd2','data_ave2','data_sd2','cluster_num']
#     writer.writerow(title_name)
    writer = csv.writer(f, lineterminator='\n')
    writer.writerow(title_name)
    for data in l:
        writer.writerow(data)
    f.close()


def createDatabyIPaddressFile(l):
    f_name = 'data_by_ipaddress/weka/'+day+'_ipaddress' + '.text'
    f = open(f_name,'w')
    for data in l:
        f.write(str(data)+"\n")
    f.close()


#--------main処理----------------------
name, ext = os.path.splitext(os.path.basename(file_name))  # ファイル名と拡張子を分ける name:ファイル名,ext:拡張子
data = pd.read_csv(file_name).values.tolist()  # ファイル読み込み
ip_num = pd.read_csv(file_name, usecols=['ip_number']).values  # データ量だけを
lst = comparisionIP(ip_num)
all_data_list = dataSet(data,lst)
data_format_list = dataFormatSet(all_data_list)
createCSVFile(data_format_list)

