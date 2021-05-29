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
    user="debian-sys-maint",  #帳號
    password="XI9BNrhAuluqvv1k", #密碼
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
                    # print((row[0][-3:]).lower())  
                    data_dic["images"]=img_data  
            data={"data": data_dic}

            #透過session紀錄使用狀態
            session['id'] = data_dic["id"]
            session['name'] = data_dic["name"]
            session['address'] = data_dic["address"]
            session['image'] = data_dic["images"]
            

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
                    "id": session['userid'],
                    "name": session['username'],
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

                #透過session紀錄使用狀態
                session['status'] = 'login'  #使用狀態
                session['userid'] = record[0] #id
                session['username'] = record[1] #name
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


#預定行程:未確認api============================================
@app.route("/api/booking", methods=["GET"])
def inbooking():
    # 登入
    try:
        if session['status'] == 'login':
            # booking資料庫資料判斷-----
            if mydb.is_connected():
                #操作方法
                mycursor=mydb.cursor()
                #使用者
                print("使用者id: ",session['userid'])
                #中繼表:抓取使用者的訂單(可能一筆以上)
                sql="SELECT * FROM signup_to_booking where signup_id = %s"
                val=session['userid']
                mycursor.execute(sql,(val,))
                record=mycursor.fetchall()
                print(record)

                #有一筆以上的訂單
                if record != []:
                    result=[]
                    for i in range(len(record)):
                        #資料庫:抓取booking資料
                        bookingid=record[i][1]
                        sql="SELECT * FROM booking where Id = %s"
                        val=bookingid
                        mycursor.execute(sql,(val,))
                        record_booking=mycursor.fetchone()
                        print(record_booking)

                        #資料庫:抓取attractions資料
                        attractionsid=record_booking[1]
                        sql="SELECT * FROM attractions where RowNumber = %s"
                        val=attractionsid
                        mycursor.execute(sql,(val,))
                        record_attractions=mycursor.fetchone()
                        #資料庫:抓取attractions url 圖片資料
                        sql_img="SELECT * FROM attractions_url where RowNumber = %s"
                        val=attractionsid
                        mycursor.execute(sql_img,(val,))
                        record_img=mycursor.fetchall()
                        img_data=[]
                        for row in record_img:
                            if ((row[1][-3:]).lower())== "jpg" or ((row[1][-3:]).lower())== "png":
                                img_data.append(row[1]) 
                        

                        # 建立booking API
                        data_dic={}
                        attraction_dic={}
                        attraction_dic["id"]=record_attractions[0]
                        attraction_dic["name"]=record_attractions[1]
                        attraction_dic["address"]=record_attractions[4]
                        attraction_dic["image"]= img_data[0]
                        data_dic["attraction"]=attraction_dic
                        data_dic["date"]=record_booking[2]
                        data_dic["time"]=record_booking[3]
                        data_dic["price"]=record_booking[4]
                        result.append(data_dic)

                    booking_data={"data":result}
                    print(booking_data)

                    #回應有資料
                    response = app.response_class(json.dumps(booking_data, ensure_ascii= False),status=200,mimetype='application/json')
                    return response

                # 使用者無訂單
                else:
                    #回應無資料: null 
                    null = None
                    booking_data = {"data":null}
                    print("無資料")
                    response = app.response_class(json.dumps(booking_data, ensure_ascii= False),status=200,mimetype='application/json')
                    return response 
    #未登入系統，拒絕存取
    except Error as error:
        booking_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
            }
        response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=403,mimetype='application/json')
        return response  

#預定行程:新行程api============================================\
@app.route("/api/booking", methods=["POST"])
def booked():
    #POST方法:
    data = request.get_json(force=True)
    attractionId = data['attractionId']
    date = data['date']
    time = data['time']
    price = data['price']

    
    #資料庫處理**************************************
    try:
        # 使用者狀態
        status=session.get('status')
        # 登入
        if status == 'login':
            #登入且建立成功
            if mydb.is_connected():
                mycursor=mydb.cursor()
                #建立booking資料----------------------------
                # mycursor.execute("DROP TABLE booking")
                # sql="CREATE TABLE booking (Id INT NOT NULL AUTO_INCREMENT, attractionId VARCHAR(255) NOT NULL, date VARCHAR(255) NOT NULL, time VARCHAR(255) NOT NULL, price VARCHAR(255) NOT NULL, PRIMARY KEY(Id))"
                # mycursor.execute(sql)
                #操作SQL:資料表booking中新增資料
                sql="INSERT INTO booking (attractionId, date, time, price) VALUES (%s,%s,%s,%s)"
                val=(attractionId, date, time, price)
                mycursor.execute(sql,val)
                mydb.commit()


                # 預定成功
                booking_success = {
                    "ok": True,
                    }
                
                #抓取booking訂單的id
                sql="SELECT last_insert_id();"
                mycursor.execute(sql)
                record=mycursor.fetchone()
                bookingId=record[0]

                # 建立中繼表(signup資料表 vs booking資料表)=======
                # 操作SQL:建立新資料表
                # mycursor.execute("DROP TABLE signup_to_booking")
                # sql="CREATE TABLE signup_to_booking (signup_id INT NOT NULL, booking_id INT NOT NULL, FOREIGN KEY (signup_id) REFERENCES signup (Id) ON DELETE RESTRICT ON UPDATE CASCADE, FOREIGN KEY (booking_id) REFERENCES booking (Id) ON DELETE RESTRICT ON UPDATE CASCADE, PRIMARY KEY (signup_id, booking_id))"
                # mycursor.execute(sql)
 
                sql="INSERT INTO signup_to_booking (signup_id, booking_id) VALUES (%s,%s)"
                val=(session['userid'], bookingId)  
                mycursor.execute(sql,val)
                mydb.commit()
                    

                #透過session紀錄使用狀態
                session['date'] = date 
                session['time'] = time 
                session['price'] = price 


                #導向成功取得資料的json格式
                response = app.response_class(json.dumps(booking_success, ensure_ascii= False),status=200,mimetype='application/json')
                return response
            #登入、建立失敗，輸入不正確或其他原因
            else:
                #註冊失敗
                booking_fail = {
                    "error": True,
                    "message": "建立失敗，輸入不正確或其他原因"
                    }
                response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=400,mimetype='application/json')
                return response  
        # 未登入
        else:
            #註冊失敗
            booking_fail = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=403,mimetype='application/json')
            return response  
    # 當資料未重覆: 連線失敗，導向失敗頁面，顯示"帳號已經被註冊"訊息
    except Error as error:
        #伺服器內部錯誤
        booking_fail = {
        "error": True,
        "message": "請填寫行程資料"
        }
        response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response  

    #資料庫處理**************************************

#預定行程:刪除api============================================
@app.route("/api/booking", methods=["DELETE"])
def delBooked():
    data = request.get_json(force=True)
    del_order = data['number']
    
    status=session.get('status')
    if status == "login":
        if mydb.is_connected():
            #操作方法
            mycursor=mydb.cursor()
            #操作SQL:取得刪除訂單的id----------------
            sql="select Id from booking limit %s,1"
            val=del_order
            mycursor.execute(sql,(val,))
            del_id=mycursor.fetchone()

            #操作SQL:刪除中繼表的訂單資料----------------
            sql="DELETE from signup_to_booking where booking_id = %s"
            val=del_id
            mycursor.execute(sql,val)
            mydb.commit()
            sql="DELETE from booking where Id =%s"
            val=del_id
            mycursor.execute(sql,val)
            mydb.commit()


            # 刪除成功
            del_success = {
                "ok": True,
                }
            response = app.response_class(json.dumps(del_success, ensure_ascii= False),status=200,mimetype='application/json')
            return response
                #登入、建立失敗，輸入不正確或其他原因
        else:
            #註冊失敗
            del_fail = {
                "error": True,
                "message": "資料刪除失敗"
                }
            response = app.response_class(json.dumps(del_fail, ensure_ascii= False),status=400,mimetype='application/json')
            return response  
    else:
        # 未登入系統，拒絕存取
        del_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
            }
        response = app.response_class(json.dumps(del_fail, ensure_ascii= False),status=403,mimetype='application/json')
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


app.run(host="0.0.0.0", port=3000, debug = True)