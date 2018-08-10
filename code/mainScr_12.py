#/usr/bin python3.6
__AUTHOR__='xia'
# -*-coding:utf-8-*-
from six.moves import urllib
from bs4 import BeautifulSoup
from bs4.diagnose import diagnose
from prettytable import PrettyTable
import re
import os
import datetime as dt
import pymysql
from sqlalchemy import create_engine
def get_info(url):
    file=open(url,'r',encoding='utf-8')
    html=file.read()
    bsObj=BeautifulSoup(html,'html.parser')
    list=bsObj.find_all(name="tr",attrs={"style":re.compile(r"background-color:(\s\w+)?")})
    count=len(list)
    print(count)



    f=open('info2.txt','a+')

    for i in range(count):
        #以下输出硬盘信息
        # print(i)
        table=bsObj.find_all(name="tr",attrs={"style":re.compile(r"background-color:(\s\w+)?")})[i]
        daname=table.select('td')[0].get_text()#框号0
        caowei=table.select('td')[1].get_text()#槽位1
        disktype=table.select('td')[2].get_text()#磁盘类型2
        hardtype=table.select('td')[4].get_text()#硬盘型号4
        sequence=table.select('td')[6].get_text()#序列号6
        score=table.select('td > span')[0].get_text()#得分7
        info = daname+" "+caowei+" "+disktype+" "+hardtype+" "+sequence+" "+score+" "
        if disktype=='SAS':
            #这里输出详情信息
            errorevent = bsObj.select('table[class="score_table"]')[i].select('td')[1].get_text()#硬盘例外事件信息
            readerr = bsObj.select('table[class="score_table"]')[i].select('td')[3].get_text()#读的错误次数
            writeerr = bsObj.select('table[class="score_table"]')[i].select('td')[5].get_text()#写的错误次数
            checkerr = bsObj.select('table[class="score_table"]')[i].select('td')[7].get_text()#校验的错误次数
            reflect = bsObj.select('table[class="score_table"]')[i].select('td')[9].get_text()#重映射扇区
            errchannel = bsObj.select('table[class="score_table"]')[i].select('td')[11].get_text()#后台扫描出的坏道信息

            info +=errorevent+" "+readerr+" "+writeerr+" "+checkerr+" "+reflect+" "+errchannel+"\r\n"
            # f.write("%s"%(info))
        if disktype=='SSD':
            exceptinfo = bsObj.select('table[class="score_table"]')[i].select('td')[1].get_text()#异常信息记录页
            badblock = bsObj.select('table[class="score_table"]')[i].select('td')[3].get_text()#坏块比例
            liferate = bsObj.select('table[class="score_table"]')[i].select('td')[5].get_text()#寿命比例
            info +=exceptinfo+" "+badblock+" "+liferate+""+"0"+" "+"0"+" "+"0"+"\r\n"
        f.write("%s"%(info))
        print("正在写入第"+str(i)+"条信息")
    print("写入文件成功！")

    #将txt文件存入数据库
    input = open('info2.txt')
    db = pymysql.connect('localhost','root','123','huawei')
    cur=db.cursor()
    for line in input.readlines():
        linelist = line.split(' ')
        sql ="INSERT INTO disk" \
                     "(daname,caowei,disktype,hardtype,sequence,score,errorevent,readerr,writeerr,checkerr,reflect,errchannel)" \
                     "VALUES" \
                     "('"+linelist[0]+"','"+linelist[1]+"','"+linelist[2]+"','"+linelist[3]+"','"+linelist[4]+"','"+linelist[5]\
                    +"','"+linelist[6]+"','"+linelist[7]+"','"+linelist[8]+"','"+linelist[9]+"','"+linelist[10]+"','"+linelist[11]+"')"
        cur.execute(sql)
        db.commit()
    print("信息插入数据库成功！")
    #去除数据库中的重复信息
    # sql1 = "create table temp as (select distinct daname,caowei,disktype,hardtype,sequence,score,errorevent,readerr,writeerr,checkerr,reflect,errchannel from disk)"
    # cur.execute(sql1)
    # sql2 = "delete from disk;"
    # cur.execute(sql2)
    # sql3 = "insert into disk select * from temp"
    # cur.execute(sql3)
    # db.commit()
    # print("已将重复信息去除")

#读取目录下的文件列表
# sPath4File="/home/xia/python/myproject"
# lsFileList=os.listdir(sPath4File)
# today = dt.datetime.today()
# oneday=dt.timedelta(days=0)
# yesterday=today-oneday
# # #文件名格式为空格+V
# format=' V'
# yes=yesterday.strftime(format)
# for sFileName in lsFileList:
#     if str.find(sFileName,yes ) >= 0:
#         sPathFileName=sPath4File+"/"+sFileName
#         print("开始读取文件")
#         print(sPathFileName)
#         get_info(sPathFileName)
get_info('/home/xia/python/myproject/diskDataCollection/2102350FJF10J300001518500 V31533631265000.html')
# get_info('/home/xia/python/myproject/2102350FJF10J300001518500 V31533631265000.html')
