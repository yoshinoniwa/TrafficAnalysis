from scipy.io import arff
import numpy as np
import glob
import pandas as pd
import os
import csv
from astropy.io.ascii.ui import write
from astropy.io.fits.convenience import writeto
from statsmodels.compat.numpy import npc_unique
from builtins import len

day = "19-02-20"
csv_original_file_name =  "wireshark_data/"+day+"_time/*"
csv_original_file_list = glob.glob(csv_original_file_name)  # 読み込むフォルダ
arff_file_name = "data_by_ipaddress/"+day+"/weka_result/*"
arff_file_list = glob.glob(arff_file_name)  # 読み込むフォルダ

csv_created_file_name ="data_by_ipaddress/"+day+"/toCSV/*"
csv_created_file_list = glob.glob(csv_created_file_name)
save_file_path = "data_by_ipaddress/"+day+"/toCSV/"

arff_list = list()
original_csv_list = list()
created_csv_list = list()
ip_and_data_list = list()
l1_list = list()
l2_list = list()
l3_list = list()
l4_list = list()
l5_list = list()


# Arff→CSV
def toCsv(content):
    data = False
    header = ""
    newContent = []
    for line in content:
        if not data:
            if "@attribute" in line:
                attri = line.split()
                columnName = attri[attri.index("@attribute")+1]
                header = header + columnName + ","
            elif "@data" in line:
                data = True
                header = header[:-1]
                header += '\n'
                newContent.append(header)
        else:
            newContent.append(line)
    return newContent

# Main loop for reading and writing files
def writeToCSV():
    for file in arff_file_list:
        with open(file , "r") as inFile:
            content = inFile.readlines()
            name,ext = os.path.splitext(os.path.basename(inFile.name))
#             os.path.splitext(inFile.name)
            new = toCsv(content)
            print(name)
            with open(save_file_path+name+".csv", "w") as outFile:
                outFile.writelines(new)
#比較もとのCSVデータ参照
def readOriginalCsvFile():
    for filename in csv_original_file_list:
        data = pd.read_csv(filename)  # ファイル読み込み
        name,ext = os.path.splitext(os.path.basename(filename))
        lst = pd.read_csv(filename).values.tolist()
        file_obj = [name,lst]
        ip_and_data_list.append(file_obj)
        original_csv_list.append(lst)
        dict = {'ipaddress' : "csvファイル"}
#         print(name)
        dict[name] = lst
#         print(dict)
#         print(len(lst))
    for f in ip_and_data_list:
        dict[f[0]] = f[1]
    return dict
 
#ARFFファイルからCSVファイル変換したファイルの参照
def readCreatedCsvFile():
    for filename in csv_created_file_list:
        data = pd.read_csv(filename)  # ファイル読み込み
        name,ext = os.path.splitext(os.path.basename(filename))
        lst = pd.read_csv(filename).values.tolist()
        created_csv_list.append(lst)
        comparisonClass(lst,name)
#         print(lst)
#         print(created_csv_list)

#クラスごとにリストを作る(例IP:8.8.8.8のクラスタ1,クラスタ2ごとにリストを作る)
#l:wekaから取得したファイル　name:IP
def comparisonClass(l,name):
#     print(c_list)

    
    class_list = list() #クラスを入れる
    l1 = list() #クラスタ1のデータ量
    l2 = list() #クラスタ2のデータ量
    l3 = list() #クラスタ3のデータ量
    l4 = list() #クラスタ4のデータ量
    l5 = list() #クラスタ5のデータ量
    
    #class_listにクラスを入れる
    for s in l:
        cls = s[2]
        class_list.append(cls)
    c_unique = list(set(class_list)) #重複したオブジェクトの削除
    num = len(c_unique)
    
    for s in l:
        if s[2] in c_unique[0]:
            l1.append(s[1])    
        if num > 1:
            if s[2] in c_unique[1]:
                l2.append(s[1])
        if num > 2:
            if s[2] in c_unique[2]:
                l3.append(s[1])
        if num > 3:
            if s[2] in c_unique[3]:
                l4.append(s[1])
        if num > 4:
            if s[2] in c_unique[4]:
                l5.append(s[1])
    print(name)
    print(l1)    
#     print(l2)
    l1_list.append(l1)
    l2_list.append(l2)
    l3_list.append(l3)
    l4_list.append(l4)
    l5_list.append(l5)
    comparisonCSV(l1,l2,l3,l4,l5,name)
    return c_unique       

#元のCSVファイルとクラスごとにまとめられたデータを比べる
def comparisonCSV(l1,l2,l3,l4,l5,name):
    print(len(l1))
    print(len(l2))
    print(len(l3))
    print(len(l4))
    print(len(l5))
    origi_csv_dict = readOriginalCsvFile()
#     print(len(origi_csv_dict))
    flag1 = 'false'
    flag2 = 'false'
    flag3 = 'false'
    flag4 = 'false'
    flag5 = 'false'
#     print(l3)
    origi_list = origi_csv_dict[name]
#     print(len(origi_list))
    csv_list1 = list()
    csv_list2 = list()
    csv_list3 = list()
    csv_list4 = list()
    csv_list5 = list()
    count = 0;
    for origin in origi_list:
#         csv_list1.append(origin[1])
        if len(l1)>0:
            for l in l1:
                if origin[1] == l:
                    flag1 = 'true'
                    break
                else:
                    flag1 = 'false'
            if flag1 == 'true':
                csv_list1.append(origin[1])
            elif flag1 == 'false':
                csv_list1.append(0)
        
        if len(l2)>0:
            for l in l2:
                if origin[1] == l:
                    flag2 = 'true'
                    count += 1
                    break
                else:
                    flag2 = 'false'
            if flag2 == 'true':
                csv_list2.append(origin[1])
            elif flag2 == 'false':
                csv_list2.append(0)
                
        if len(l3)>0:
            for l in l3:
                if origin[1] == l:
                    flag3 = 'true'
                    break
                else:
                    flag3 = 'false'
            if flag3 == 'true':
                csv_list3.append(origin[1])
            elif flag3 == 'false':
                csv_list3.append(0)
                    
        if len(l4)>0:
            for l in l4:
                if origin[1] == l:
                    flag4 = 'true'
                    break
                else:
                    flag4 = 'false'
            if flag4 == 'true':
                csv_list4.append(origin[1])
            elif flag4 == 'false':
                csv_list4.append(0)
            
        if len(l5)>0:
            for l in l5:
                if origin[1] == l:
                    flag5 = 'true'
                    break
                else:
                    flag5 = 'false'
            if flag5 == 'true':
                csv_list5.append(origin[1])
            elif flag5 == 'false':
                csv_list5.append(0)
    print("-------")
    print(count)            
    #-----------------------------------------       
    list1 = list()
    list2 = list()
    list3 = list()
    list4 = list()
    list5 = list()  
     
    value1 = 'No. ,length'
    count1=0
    list1.append(value1)
    for n in csv_list1:
        value1 = str(count1) + ',' + str(n)
        list1.append(value1)
        count1 += 1
    createCSVFile(list1,name,'1')    
     
    if len(csv_list2) > 1:
        value2 = 'No. ,length'
        count2=0
        list2.append(value2)
        for n in csv_list2:
            value2 = str(count2) + ',' + str(n)
            list2.append(value2)
            count2 += 1
        createCSVFile(list2,name,'2')     
       
    if len(csv_list3) > 1:
        value3 = 'No. ,length'
        count3=0
        list3.append(value3)
        for n in csv_list3:
            value3 = str(count3) + ',' + str(n)
            list3.append(value3)
            count3 += 1
        createCSVFile(list3,name,'3') 
     
    if len(csv_list4) > 1:
        value4 = 'No. ,length'
        count4=0
        list4.append(value4)
        for n in csv_list4:
            value4 = str(count4) + ',' + str(n)   
            list4.append(value4)
            count4 += 1
        createCSVFile(list4,name,'4')  
      
    if len(csv_list5) > 1:
        value5 = 'No. ,length'
        count5=0
        list5.append(value5)
        for n in csv_list5: 
            value5 = str(count5) + ',' + str(n)       
            list5.append(value5)
            count5 += 1
        createCSVFile(list5,name,'1')
    #-----------------------------------------
def createCSVFile(l,name,num):
    f_name = "data_by_ipaddress/"+day+"/cluster/"+name+"_"+num+".csv"
    f = open(f_name,'w')
    for data in l:
        f.write(str(data)+"\n")
    f.close()    
        


writeToCSV()
readOriginalCsvFile()
readCreatedCsvFile()
print("========")
print(len(original_csv_list))
print(len(l1_list))
# print(created_csv_list)
