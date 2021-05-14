from flask import *
import mysql.connector
from mysql.connector import Error
import json
app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True
#session產生金鑰
#comand: python -c 'import os; print(os.urandom(16))'
app.secret_key='secret'

#資料庫連線
mydb = mysql.connector.connect(
    host="localhost",    #主機名稱
    user="root",  #帳號
    password="ELSA2700", #密碼
    database="travel",     #使用資料庫
)

mycursor = mydb.cursor()

#景點api
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


#取得當前資訊api=====================================================
@app.route("/api/user", methods = ["GET"])
def getState():
    #透過session紀錄使用狀態
    status=session.get('status')
    print("目前狀態為: ",status)
    try:
        if status == 'login':
            #登入成功
            login_sta = {
                "data": {
                    "id": session['id'],
                    "name": session['name'],
                    "email": session['email']
                    }
                }

            #導向成功取得資料的json格式
            response = app.response_class(json.dumps(login_sta, ensure_ascii= False),status=200,mimetype='application/json')
            return response
        else:
            #登入失敗
            null = None
            unlogin_sta = {"data":null}
            response = app.response_class(json.dumps(unlogin_sta, ensure_ascii= False),status=400,mimetype='application/json')
            return response  
    except Error as error:
        #登入失敗
        null = None
        unlogin_sta = {"data":null}
        response = app.response_class(json.dumps(unlogin_sta, ensure_ascii= False),status=500,mimetype='application/json')
        return response  

#註冊新會員api=====================================================
@app.route("/api/user", methods=["POST"])
def signup():
    #POST方法:取得會員的註冊資料
    data = request.get_json(force=True)
    name = data['name']
    email = data['email']
    password = data['password']

    print("姓名: ", name,"信箱: ", email, "密碼: ", password)

    #資料庫處理**************************************
    try:
        #當連線成功，執行下列程式碼
        if mydb.is_connected():
            #操作方法
            mycursor=mydb.cursor()
            #資料庫帳號username 設為UNIQUE:決定帳號名稱是否重複
            # 操作SQL:建立新資料表----------------
            # mycursor.execute("DROP TABLE signup")
            # sql="CREATE TABLE signup (Id INT NOT NULL AUTO_INCREMENT, username VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, password VARCHAR(255) NOT NULL, UNIQUE (email), PRIMARY KEY(Id))"
            # mycursor.execute(sql)
            #操作SQL:資料表signup中新增資料----------------
            sql="INSERT INTO signup (username, email, password) VALUES (%s,%s,%s) "
            val=(name, email, password)
            if name != "" and email != "" and password != "":
                mycursor.execute(sql,val)
                mydb.commit()

                # 註冊成功
                signup_success = {
                    "ok": True,
                    "message": "註冊成功，請登入系統"
                    }

                #導向成功取得資料的json格式
                response = app.response_class(json.dumps(signup_success, ensure_ascii= False),status=200,mimetype='application/json')
                return response
            else:
                #註冊失敗
                signup_fail = {
                    "error": True,
                    "message": "不可填入空白"
                    }
                response = app.response_class(json.dumps(signup_fail, ensure_ascii= False),status=400,mimetype='application/json')
                return response 


        else:
            #註冊失敗
            signup_fail = {
                "error": True,
                "message": "Email 已經註冊帳戶"
                }
            response = app.response_class(json.dumps(signup_fail, ensure_ascii= False),status=400,mimetype='application/json')
            return response  

    # 當資料未重覆: 連線失敗，導向失敗頁面，顯示"帳號已經被註冊"訊息
    except Error as error:
        #註冊失敗
        signup_fail = {
        "error": True,
        "message": "Email 已經註冊帳戶"
        }
        response = app.response_class(json.dumps(signup_fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response  

    #資料庫處理**************************************

#登入api=====================================================
@app.route("/api/user", methods=["PATCH"])
def signin():
    #取得會員的註冊資料
    data = request.get_json(force=True)
    email = data['email']
    password = data['password']
    print("信箱: ", email, "密碼: ", password)

    #資料庫處理**************************************
    try:
        #當連線成功，執行下列程式碼
        if mydb.is_connected():
            #操作方法
            mycursor=mydb.cursor()

            #查詢使用者輸入的帳號、密碼:有對應結果 
            #操作SQL:查詢資料表----------------
            sql="SELECT * FROM signup WHERE email = %s and password = %s"
            val=(email, password)
            mycursor.execute(sql,val)

            #從資料庫搜尋到的查詢結果
            record=mycursor.fetchone()
            print("使用者登入資料: ",record)
            if record != None:
                #登入成功
                signin_success = {
                    "ok": True
                }

                # #透過session紀錄使用狀態
                session['status'] = 'login'  #使用狀態
                session['id'] = record[0] #id
                session['name'] = record[1] #name
                session['email'] =record[2] #email


                #導向成功取得資料的json格式
                response = app.response_class(json.dumps(signin_success, ensure_ascii= False),status=200,mimetype='application/json')
                return response
            else:
                #登入失敗
                signin_fail = {
                    "error": True,
                    "message": "自訂的錯誤訊息"
                    }

                #透過session紀錄使用狀態
                session['status'] = 'unlogin'  #使用狀態
                response = app.response_class(json.dumps(signin_fail, ensure_ascii= False),status=400,mimetype='application/json')
                return response  

    # 當資料未重覆: 連線失敗，導向失敗頁面，顯示"帳號已經被註冊"訊息
    except Error as error:
        # 登入失敗
        signin_fail = {
        "error": True,
        "message": "自訂的錯誤訊息"
        }
        response = app.response_class(json.dumps(signin_fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response  

    #資料庫處理**************************************


#登出api=====================================================
@app.route("/api/user", methods=["DELETE"])
def signout():
    session['status']='unlogin'
    # 登出成功
    signout_success = {
        "ok": True,
        }
    response = app.response_class(json.dumps(signout_success, ensure_ascii= False),status=200,mimetype='application/json')
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

# host="0.0.0.0", 
app.run(port=3000, debug = True)