import csv
import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
 
from pathlib import Path
from blaze.tests.dont_test_mongo import file_name

# path = Path("2018-11-1815_time/") #ファイルパスの設定
# filelist = list(path.glob("*"))


filelist = glob.glob("2018-11-1815_minute/*") #読み込むフォルダ
extension = '.png' #拡張子
file_path = 'resultFigure/2018-11-1815_minute/combine/' #図の保存先
#フォルダ内にあるcsvファイルを読み込む
for csvfilename in filelist:
#     plt.clf()
    print(csvfilename)
    name,ext = os.path.splitext(os.path.basename(csvfilename))
    print(name)
    data = pd.read_csv(csvfilename)
    left = data['No. ']  #横軸の設定
    height = data['length'] #縦軸の設定
    plt.title(csvfilename) #タイトルの設定
    plt.plot(left,height) #図の作成
#     plt.show() #図の表示
    plt.savefig(file_path+name+extension) #図の保存
    
print(filelist)


# ファイルの読み込み
# def callFile():
#     with open(path) as fp:
#         csv_list = list(csv.reader(fp))

#平均
# def average():
    
#分散

 


# callFile()