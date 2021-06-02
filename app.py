from flask import *
import mysql.connector
from mysql.connector import Error
import json, requests
from mysql.connector.pooling import MySQLConnectionPool

app=Flask(__name__)

app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True


app.secret_key='secret'

#資料庫連線
dbconfig = {
  "host": "localhost",
  "user":"root",
  "password":"ELSA2700",
  "database":"travel"
}
mydb1 = mysql.connector.connect(pool_name ="mypool",pool_size = 6,**dbconfig)

#景點api
@app.route("/api/attractions", methods=["GET"])
def attractions():
    page=request.args.get("page",0)
    page=int(page)
    keyword=request.args.get("keyword","")



    #資料庫處理**************************************
    mydb1 = mysql.connector.connect(pool_name = "mypool")
    mycursor=mydb1.cursor()
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
            mydb1.close()
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response
        else:
            data={"nextPage":None,"data":[]}
            mydb1.close()
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response           
    except:
        fail = {
        "error":True,
        "message": "自訂的錯誤訊息"
        }
        mydb1.close()
        response = app.response_class(json.dumps( fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response

@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    #資料庫處理**************************************
    mydb2 = mysql.connector.connect(pool_name = "mypool")
    mycursor=mydb2.cursor()
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
            
            mydb2.close()
            response = app.response_class(json.dumps( data, ensure_ascii= False),status=200,mimetype='application/json')
            return response
        else:
            fail = {
            "error":True,
            "message": "自訂的錯誤訊息"
            }
            mydb2.close()
            response = app.response_class(json.dumps( fail, ensure_ascii= False),status=400,mimetype='application/json')
            return response
    except:
        fail = {
        "error":True,
        "message": "自訂的錯誤訊息"
        }
        mydb2.close()
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
            cnx3 = mysql.connector.connect(pool_name = "mypool")
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
                # cnx.close()
                return response
            else:
                #註冊失敗
                signup_fail = {
                    "error": True,
                    "message": "不可填入空白"
                    }
                response = app.response_class(json.dumps(signup_fail, ensure_ascii= False),status=400,mimetype='application/json')
                # cnx.close()
                return response 


        else:
            #註冊失敗
            signup_fail = {
                "error": True,
                "message": "Email 已經註冊帳戶"
                }
            response = app.response_class(json.dumps(signup_fail, ensure_ascii= False),status=400,mimetype='application/json')
            cnx3.close()
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
        #操作方法
        mydb3 = mysql.connector.connect(pool_name = "mypool")
        mycursor=mydb3.cursor()

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
            mydb3.close()
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
            mydb3.close()
            response = app.response_class(json.dumps(signin_fail, ensure_ascii= False),status=400,mimetype='application/json')
            return response  

    # 當資料未重覆: 連線失敗，導向失敗頁面，顯示"帳號已經被註冊"訊息
    except Error as error:
        # 登入失敗
        signin_fail = {
        "error": True,
        "message": "自訂的錯誤訊息"
        }
        mydb3.close()
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
            #操作方法
            mydb4 = mysql.connector.connect(pool_name = "mypool")
            mycursor=mydb4.cursor()
            #查詢要查詢的會員帳號
            #操作SQL:查詢資料表(單一參數)----------------
            sql="SELECT * FROM booking"
            mycursor.execute(sql)
            #從資料庫搜尋到的查詢結果
            record=mycursor.fetchall()
            print(record)
            if record != []:
                # booking資料
                booking_data = {
                    "data": {
                        "attraction": {
                            "id": session['id'],
                            "name": session['name'],
                            "address": session['address'],
                            "image": session['image']
                            },
                        "date": session['date'],
                        "time": session['time'],
                        "price": session['price']
                    }
                }
                #回應有資料
                mydb4.close()
                response = app.response_class(json.dumps(booking_data, ensure_ascii= False),status=200,mimetype='application/json')
                return response
            else:
                #回應無資料: null 
                null = None
                booking_data = {"data":null}
                mydb4.close()
                response = app.response_class(json.dumps(booking_data, ensure_ascii= False),status=200,mimetype='application/json')
                return response 
    #未登入系統，拒絕存取
    except Error as error:
        booking_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
            }
        mydb4.close()
        response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=403,mimetype='application/json')
        return response  

#預定行程:新行程api============================================
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
            mydb5 = mysql.connector.connect(pool_name = "mypool")
            mycursor=mydb5.cursor()
            if mydb5.is_connected():
                #建立booking資料----------------------------
                # mycursor.execute("DROP TABLE signup")
                # sql="CREATE TABLE booking (Id INT NOT NULL AUTO_INCREMENT, attractionId VARCHAR(255) NOT NULL, date DATE NOT NULL, time VARCHAR(255) NOT NULL, price VARCHAR(255) NOT NULL, PRIMARY KEY(Id))"
                # mycursor.execute(sql)
                #操作SQL:資料表booking中新增資料
                sql="INSERT INTO booking (attractionId, date, time, price) VALUES (%s,%s,%s,%s)"
                val=(attractionId, date, time, price)
                mycursor.execute(sql,val)
                mydb5.commit()
                # 預定成功
                booking_success = {
                    "ok": True,
                    }
            

                #透過session紀錄使用狀態
                session['date'] = date 
                session['time'] = time 
                session['price'] = price 


                #導向成功取得資料的json格式
                mydb5.close()
                response = app.response_class(json.dumps(booking_success, ensure_ascii= False),status=200,mimetype='application/json')
                return response
            #登入、建立失敗，輸入不正確或其他原因
            else:
                #註冊失敗
                booking_fail = {
                    "error": True,
                    "message": "建立失敗，輸入不正確或其他原因"
                    }
                mydb5.close()
                response = app.response_class(json.dumps(booking_fail, ensure_ascii= False),status=400,mimetype='application/json')
                return response  
        # 未登入
        else:
            #未登入失敗
            booking_fail = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            mydb5.close()
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
    status=session.get('status')
    if status == "login":
        #操作方法
        mydb6 = mysql.connector.connect(pool_name = "mypool")
        mycursor=mydb6.cursor()
        if mydb6.is_connected():
            #操作SQL:資料表booking中新增資料----------------
            sql="DELETE from booking"
            mycursor.execute(sql)
            mydb6.commit()

            # 刪除成功
            del_success = {
                "ok": True,
                }
            mydb6.close()
            response = app.response_class(json.dumps(del_success, ensure_ascii= False),status=200,mimetype='application/json')
            return response
            #登入、建立失敗，輸入不正確或其他原因
        else:
            #註冊失敗
            del_fail = {
                "error": True,
                "message": "資料刪除失敗"
                }
            mydb6.close()
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

#訂單建立:清單api============================================
@app.route("/api/orders", methods=["POST"])
def order():
    try:
        # 登入
        status = session.get('status')
        if status == 'login':
            #POST方法:
            data = request.get_json(force=True)
            prime = data['prime']

            # 紀錄訂單狀態
            session['order'] = "unpaid"
            session['contact_name'] = data['order']['contact']['name']
            session['contact_email'] = data['order']['contact']['email']
            session['contact_phone'] = data['order']['contact']['phone']

            # 訂單建立失敗
            if session['contact_name'] == "" or session['contact_email'] == "" or session['contact_phone'] == "":
                # 訂單失敗
                order_fail = {
                    "error": True,
                    "message": "訂單建立失敗，輸入不正確或其他原因"
                    }

                response = app.response_class(json.dumps(order_fail, ensure_ascii= False),status=400,mimetype='application/json')
                return response
            # 訂單建立成功
            else:
                #tappay server 連線-------
                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                headers = {'content-type':'application/json','x-api-key':'partner_D7xWITe3QnKxgA4p6ZIJrvkKLzyAkdRybJQeIw3RZKvjtgDnLSHjdxRu'}
                data = {
                    "prime": prime,
                    "partner_key": 'partner_D7xWITe3QnKxgA4p6ZIJrvkKLzyAkdRybJQeIw3RZKvjtgDnLSHjdxRu',
                    "merchant_id": "Chiao_ESUN",
                    "details":"TapPay Test",
                    "amount": 100,
                    "cardholder": {
                        "phone_number": "+886923456789",
                        "name": "王小明",
                        "email": "LittleMing@Wang.com",
                        "zip_code": "100",
                        "address": "台北市天龍區芝麻街1號1樓",
                        "national_id": "A123456789"
                        },
                    }

                req = requests.post(url, data=json.dumps(data), headers=headers)
                result = json.loads(req.text)

                # 付款成功
                if result['status'] == 0:
                    # 紀錄訂單狀態:已付款
                    session['order'] = "paid"
                    pay_success = {
                        "data": {
                            "number": result['rec_trade_id'],
                            "payment": {
                            "status": 0,
                            "message": "付款成功"
                            }
                        }
                    }

                    response = app.response_class(json.dumps(pay_success, ensure_ascii= False),status=200,mimetype='application/json')
                    return response
                else:
                    # 付款失敗
                    pay_fail = {
                        "data": {
                            "number": result['rec_trade_id'],
                            "payment": {
                            "status": 1,
                            "message": "付款失敗"
                            }
                        }
                    }

                    response = app.response_class(json.dumps(pay_fail, ensure_ascii= False),status=200,mimetype='application/json')
                    return response
        else:
            #未登入失敗
            order_fail = {
                "error": True,
                "message": "未登入系統，拒絕存取"
                }
            response = app.response_class(json.dumps(order_fail, ensure_ascii= False),status=403,mimetype='application/json')
            return response  
    # 當資料未重覆: 連線失敗，導向失敗頁面，顯示"帳號已經被註冊"訊息
    except Error as error:
        #伺服器內部錯誤
        order_fail = {
        "error": True,
        "message": "伺服器內部錯誤"
        }
        response = app.response_class(json.dumps(order_fail, ensure_ascii= False),status=500,mimetype='application/json')
        return response  

@app.route("/api/order/<orderNumber>")
def orderId(orderNumber):
    # 登入
    status = session.get('status')
    if status == 'login':
        # 訂單有資料
        orderinfo = {
            "data": {
                "number": orderNumber,
                "price": session['price'],
                "trip": {
                "attraction": {
                    "id": session['id'],
                    "name": session['name'],
                    "address": session['address'],
                    "image": session['image']
                },
                "date": session['date'],
                "time": session['time']
                },
                "contact": {
                "name": session['contact_name'],
                "email": session['contact_email'],
                "phone": session['contact_phone']
                },
                "status": 1
            }
        }
        print(orderinfo)

        response = app.response_class(json.dumps(orderinfo, ensure_ascii= False),status=200,mimetype='application/json')
        return response
    else:
        #未登入失敗
        order_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
            }
        response = app.response_class(json.dumps(order_fail, ensure_ascii= False),status=403,mimetype='application/json')
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