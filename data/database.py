# #載入套件
import urllib.request as req
import json
import mysql.connector
import re

#資料庫連線
mydb = mysql.connector.connect(
    host="localhost",    #主機名稱
    user="root",         #帳號
    password="ELSA2700", #密碼
    database="travel",     #使用資料庫
)

mycursor = mydb.cursor()
 
# mycursor.execute("DROP TABLE attractions")
# mycursor.execute("CREATE TABLE attractions (RowNumber INT primary key, stitle text, CAT2 text, xbody text, address text, info text, MRT text, latitude VARCHAR(255), longitude VARCHAR(255))")



#取得json格式資料==========================================


with open("taipei-attractions.json","r",encoding="utf-8") as response:
    data = json.load(response)



json_info_list=data["result"]["results"]

#attractions 資料表: 放入圖片網址以外的資訊==========================
sql ="insert into attractions (RowNumber, stitle, CAT2, xbody, address, info, MRT, latitude, longitude) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for info in json_info_list:
    args=(info["RowNumber"],info["stitle"],info["CAT2"],info["xbody"],
    info["address"],info["info"],info["MRT"],info["latitude"],
    info["longitude"])
    mycursor.execute(sql, args)
mydb.commit()

 #attractions_url 資料表: 放入所有圖片網址的資訊==========================
# mycursor.execute("DROP TABLE attractions_url")
# mycursor.execute("CREATE TABLE attractions_url (RowNumber INT, file text, FOREIGN KEY (RowNumber) REFERENCES attractions(RowNumber) )")

sql ="insert into attractions_url (RowNumber, file) values (%s, %s)"
for info in json_info_list:
    for i in range(1,len(info["file"].split("http"))):
        pic_url="http"+info["file"].split("http")[i]
        print(info["RowNumber"],pic_url)
        args=(info["RowNumber"],pic_url)
        mycursor.execute(sql, args) 
mydb.commit()



