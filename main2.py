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
# from bitarray._bitarray import length

# グローバル変数
day = "2016-09-24"
file_name = "wireshark_data/"+day+"_time/*"
filelist = glob.glob(file_name)  # 読み込むフォルダ
extension = '.png'  # 拡張子
file_save_path = 'resultFigure/'+day+'_time/180000/'  # 図を保存するパス
all_data_list = list()
time_ave_list = list()
time_sd_list = list()
data_ave_list = list()
data_sd_list = list()
ipaddress_list = list()

ipaddress_traffic_list = list()
# time = []

# 図を作る関数
def createFigure():
    for csvfilename in filelist:
        plt.clf() #図をリセット
        print(csvfilename)
        name, ext = os.path.splitext(os.path.basename(csvfilename))  # ファイル名と拡張子を分ける name:ファイル名,ext:拡張子
        data = pd.read_csv(csvfilename)  # ファイル読み込み
        len = pd.read_csv(csvfilename, usecols=['length']).values  # データ量だけを
        if 'origin' in name:
            print(name)
        else:
            dataSet(len,name)

def dataSet(l,name):
    list_length = len(l)  # リストの長さ
    t_count = 0  # 0の時間カウント用
    time_list = list()  # タイミング格納
    len_list = list()  # データ量格納
    len_list.append('length')
    all_data = ['time_ave','time_sd','data_ave','data_var','class']
#     all_data_list.append(all_data)
    for num in l:
        # 秒数の差があるかないか
        if num == 0:
            t_count += 1  # 通信していない間の時間をカウント
        else:
            if t_count != 0: #通信していない時間があったらリストに追加
                time_list.append(t_count)
            t_count = 0
            for len_num in num: #
                len_list.append(len_num)
#                 len_list.append('\n')
#     print(len_list)
   
    print(len_list)
    if not len_list:
        print('空です')
    else:
        createDatabyIPaddressFile(name,len_list)
    
# 平均
def average(l):
    ave = mean(l)
#     difference(l, ave)
    return ave


# 偏差
def difference(l,ave):
    diff = []
    for num in l:
        diff.append(num - ave)
    return diff


# 標準偏差
def variance(l):
    ave = average(l)
    diff = difference(l,ave)
    # 偏差の二乗
    squared_diff = []
    for d in diff:
        squared_diff.append(d ** 2)
    #分散を求める
    sum_squared_diff = sum(squared_diff)
    variance = sum_squared_diff/len(l)
    sd = math.sqrt(variance)
    return sd


def createDatabyIPaddressFile(ip,l):
    print(ip)
    f_name = 'data_by_ipaddress/'+day+'/csv/'+ip+'.csv'
    f = open(f_name,'w')
    for data in l:
        f.write(str(data)+"\n")
    f.close()

createFigure()

# createIPaddressFile(ipaddress_list)
# createCSVFile(all_data_list)
print(all_data_list)



# def createCSVFile(l):
#     f_name = 'wekafile/'+day + '.csv'
#     f = open(f_name, 'a')
#     title_name = ['time_ave','time_sd','data_ave','data_sd','class']
# #     writer.writerow(title_name)
#     writer = csv.writer(f, lineterminator='\n')
#     writer.writerow(title_name)
#     for data in l:
#         writer.writerow(data)
#     f.close()
    
# def createIPaddressFile(l):
#     f_name = 'ipaddress/'+day+'.txt'
#     f = open(f_name,'w')
#     for data in l:
#         f.write(data+"\n")
#     f.close()



