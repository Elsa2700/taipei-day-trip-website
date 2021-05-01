from flask import *
import mysql.connector
from mysql.connector import Error
import json
app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

#資料庫連線
mydb = mysql.connector.connect(
    host="localhost",    #主機名稱
    user="debian-sys-maint",         #帳號
    password="XI9BNrhAuluqvv1k", #密碼
    database="travel",     #使用資料庫
)

mycursor = mydb.cursor()

#api
@app.route("/api/attractions", methods=["GET"])
def attractions():
    page=request.args.get("page",0)
    page=int(page)
    keyword=request.args.get("keyword","")



    #資料庫處理**************************************
    mycursor=mydb.cursor()
    #查詢要查詢的會員帳號
    #操作SQL:查詢資料表(單一參數)----------------
    sql="SELECT * FROM attractions where stitle like %s limit %s, %s"
    mycursor.execute(sql, (("%"+keyword+"%"),(page*12),12))
    #從資料庫搜尋到的查詢結果
    record=mycursor.fetchall()
    try:
        if len(record)>0:
            result=[]
            for i in range(len(record)):
                data_dic={}
                data_dic["id"]=record[i][0]
                data_dic["name"]=record[i][1]
                data_dic["category"]=record[i][2]
                data_dic["description"]=record[i][3]
                data_dic["address"]=record[i][4]
                data_dic["transport"]=record[i][5]
                data_dic["mrt"]=record[i][6]
                data_dic["latitude"]=record[i][7]
                data_dic["longitude"]=record[i][8]
                sql_img="SELECT file FROM attractions_url where RowNumber = %s"
                RN=(str(record[i][0]),)
                mycursor.execute(sql_img,RN)
                record_img=mycursor.fetchall()
                img_data=[]
                for row in record_img:
                    if ((row[0][-3:]).lower())== "jpg" or ((row[0][-3:]).lower())== "png":
                        img_data.append(row[0]) 
                        data_dic["images"]=img_data  
                          
  
                result.append(data_dic)
            if len(record)==12:
                page_data = (page+1)
            else:
                page_data = None
            data={"nextPage":page_data,"data":result}
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response
        else:
            data={"nextPage":None,"data":[]}
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response           
    except:
        fail = {
        "error":True,
        "message": "自訂的錯誤訊息"
        }
        response = app.response_class(json.dumps( fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response

@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    #資料庫處理**************************************
    mycursor=mydb.cursor()
    #操作SQL:查詢資料表(單一參數)----------------
    sql="SELECT * FROM attractions where RowNumber= %s"
    RN=(str(attractionId),)
    mycursor.execute(sql, RN)
    record=mycursor.fetchone()
    try:
        if len(record)>0:
            data_dic={}
            data_dic["id"]=record[0]
            data_dic["name"]=record[1]
            data_dic["category"]=record[2]
            data_dic["description"]=record[3]
            data_dic["address"]=record[4]
            data_dic["transport"]=record[5]
            data_dic["mrt"]=record[6]
            data_dic["latitude"]=record[7]
            data_dic["longitude"]=record[8]
            sql_img="SELECT file FROM attractions_url where RowNumber = %s"
            RN=(str(attractionId),)
            mycursor.execute(sql_img,RN)
            record_img=mycursor.fetchall()
            img_data=[]
            for row in record_img:
                # print((row[0][-3:]).lower())
                if ((row[0][-3:]).lower())== "jpg" or ((row[0][-3:]).lower())== "png":
                    img_data.append(row[0]) 
                    print((row[0][-3:]).lower())  
                    data_dic["images"]=img_data  
            data={"data": data_dic}
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response
        else:
            fail = {
            "error":True,
            "message": "自訂的錯誤訊息"
            }
            response = app.response_class(json.dumps( fail, ensure_ascii= False),status=400,mimetype='application/json')
            return response
    except:
        fail = {
        "error":True,
        "message": "自訂的錯誤訊息"
        }
        response = app.response_class(json.dumps( fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response

    


# Pages
@app.route("/")
def index():
	return render_template("index.html")
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


app.run(host="0.0.0.0", port=3000, debug=True)