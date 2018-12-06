import csv
import pandas as pd

path = 'tracedata/16-09-27.csv' #ファイルパスの設定


# ファイルの読み込み
def callFile():
    with open(path) as fp:
        csv_list = list(csv.reader(fp))

#平均
# def average():
    
#分散

 


callFile()