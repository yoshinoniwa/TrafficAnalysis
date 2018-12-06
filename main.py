import csv
import pandas as pd
import matplotlib.pyplot as plt
import glob
 
from pathlib import Path

# path = Path("2018-11-1815_time/") #ファイルパスの設定
# filelist = list(path.glob("*"))
filelist = glob.glob("2018-11-1815_time/*")

for csvfilename in filelist:
#     name = '2018-11-1815_time/'
#     filename = name+csvfilename
    print(csvfilename)
    data = pd.read_csv(csvfilename)
    left = data['No. ']
    height = data['length']
  
    plt.plot(left,height)
    plt.show()

print(filelist)
# ファイルの読み込み
# def callFile():
#     with open(path) as fp:
#         csv_list = list(csv.reader(fp))

#平均
# def average():
    
#分散

 


# callFile()