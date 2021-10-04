# #載入套件
import urllib.request as req
import json
import mysql.connector
import re

#資料庫連線
mydb = mysql.connector.connect(
    host="localhost",    #主機名稱
    user="debian-sys-maint",         #帳號
    password="XI9BNrhAuluqvv1k", #密碼
    database="travel",     #使用資料庫
)

mycursor = mydb.cursor()

with open("taipei-attractions.json","r",encoding="utf-8") as response:
    data = json.load(response)



json_info_list=data["result"]["results"]

sql ="insert into attractions (RowNumber, stitle, CAT2, xbody, address, info, MRT, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for info in json_info_list:
   args=(info["RowNumber"],info["stitle"],info["CAT2"],info["xbody"],
   info["address"],info["info"],info["MRT"],info["latitude"],
   info["longitude"])
   mycursor.execute(sql, args)
mydb.commit()

sql ="insert into attractions_url (RowNumber, file) values (%s, %s)"


for info in json_info_list:
    for i in range(1,len(info["file"].split("http"))):
        pic_url="http"+info["file"].split("http")[i]
        args=(info["RowNumber"],pic_url)
        mycursor.execute(sql, args) 
mydb.commit()



