from flask import *
import mysql.connector
from mysql.connector import Error
import json
import requests
from dotenv import dotenv_values
from dotenv import load_dotenv
import os
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

load_dotenv()
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('EMAIL')
app.config['MAIL_PASSWORD'] = os.getenv('EMAILPSW')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["JSON_AS_ASCII"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.secret_key = 'secret'
mail = Mail(app)


load_dotenv()

dbconfig = {
    "host": os.getenv('DB_HOST'),
    "user": os.getenv('DB_USER'),
    "password": os.getenv('DB_PSW'),
    "database": os.getenv('DBT')
}

mydb1 = mysql.connector.connect(pool_name="mypool", pool_size=7, **dbconfig)


@app.route("/api/attractions", methods=["GET"])
def attractions():
    page = request.args.get("page", 0)
    page = int(page)
    keyword = request.args.get("keyword", "")

    mydb1 = mysql.connector.connect(pool_name="mypool")
    mycursor = mydb1.cursor()
    sql = "SELECT * FROM attractions where stitle like %s limit %s, %s"
    mycursor.execute(sql, (("%"+keyword+"%"), (page*12), 12))
    record = mycursor.fetchall()
    try:
        if len(record) > 0:
            result = []
            for i in range(len(record)):
                data_dic = {}
                data_dic["id"] = record[i][0]
                data_dic["name"] = record[i][1]
                data_dic["category"] = record[i][2]
                data_dic["description"] = record[i][3]
                data_dic["address"] = record[i][4]
                data_dic["transport"] = record[i][5]
                data_dic["mrt"] = record[i][6]
                data_dic["latitude"] = record[i][7]
                data_dic["longitude"] = record[i][8]
                sql_img = "SELECT file FROM attractions_url where RowNumber = %s"
                RN = (str(record[i][0]),)
                mycursor.execute(sql_img, RN)
                record_img = mycursor.fetchall()
                img_data = []
                for row in record_img:
                    if ((row[0][-3:]).lower()) == "jpg" or ((row[0][-3:]).lower()) == "png":
                        img_data.append(row[0])
                        data_dic["images"] = img_data

                result.append(data_dic)
            if len(record) == 12:
                page_data = (page+1)
            else:
                page_data = None
            data = {"nextPage": page_data, "data": result}
            mydb1.close()
            response = app.response_class(json.dumps(
                data, ensure_ascii=False), status=200, mimetype='application/json')
            return response
        else:
            data = {"nextPage": None, "data": []}
            mydb1.close()
            response = app.response_class(json.dumps(
                data, ensure_ascii=False), status=200, mimetype='application/json')
            return response
    except:
        fail = {
            "error": True,
            "message": "自訂的錯誤訊息"
        }
        mydb1.close()
        response = app.response_class(json.dumps(
            fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/attraction/<attractionId>")
def attractionId(attractionId):
    mydb2 = mysql.connector.connect(pool_name="mypool")
    mycursor = mydb2.cursor()
    sql = "SELECT * FROM attractions where RowNumber= %s"
    RN = (str(attractionId),)
    mycursor.execute(sql, RN)
    record = mycursor.fetchone()
    try:
        if len(record) > 0:
            data_dic = {}
            data_dic["id"] = record[0]
            data_dic["name"] = record[1]
            data_dic["category"] = record[2]
            data_dic["description"] = record[3]
            data_dic["address"] = record[4]
            data_dic["transport"] = record[5]
            data_dic["mrt"] = record[6]
            data_dic["latitude"] = record[7]
            data_dic["longitude"] = record[8]
            sql_img = "SELECT file FROM attractions_url where RowNumber = %s"
            RN = (str(attractionId),)
            mycursor.execute(sql_img, RN)
            record_img = mycursor.fetchall()
            img_data = []
            for row in record_img:
                if ((row[0][-3:]).lower()) == "jpg" or ((row[0][-3:]).lower()) == "png":
                    img_data.append(row[0])
                    data_dic["images"] = img_data
            data = {"data": data_dic}

            session['id'] = data_dic["id"]
            session['name'] = data_dic["name"]
            session['address'] = data_dic["address"]
            session['image'] = data_dic["images"]

            mydb2.close()
            response = app.response_class(json.dumps(
                data, ensure_ascii=False), status=200, mimetype='application/json')
            return response
        else:
            fail = {
                "error": True,
                "message": "自訂的錯誤訊息"
            }
            mydb2.close()
            response = app.response_class(json.dumps(
                fail, ensure_ascii=False), status=400, mimetype='application/json')
            return response
    except:
        fail = {
            "error": True,
            "message": "自訂的錯誤訊息"
        }
        mydb2.close()
        response = app.response_class(json.dumps(
            fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/user", methods=["GET"])
def getState():
    status = session.get('status')
    try:
        if status == 'login':
            login_sta = {
                "data": {
                    "id": session['userid'],
                    "name": session['username'],
                    "email": session['email']
                }
            }
            response = app.response_class(json.dumps(
                login_sta, ensure_ascii=False), status=200, mimetype='application/json')
            return response
        else:
            null = None
            unlogin_sta = {"data": null}
            response = app.response_class(json.dumps(
                unlogin_sta, ensure_ascii=False), status=400, mimetype='application/json')
            return response
    except Error as error:
        null = None
        unlogin_sta = {"data": null}
        response = app.response_class(json.dumps(
            unlogin_sta, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/user", methods=["POST"])
def signup():
    data = request.get_json(force=True)
    name = data['name']
    email = data['email']
    password = data['password']

    try:
        mydb3 = mysql.connector.connect(pool_name="mypool")
        mycursor = mydb3.cursor()
        if name == "" and email == "" and password == "":
            signup_fail = {
                "error": True,
                "message": "不可填入空白"
            }
            mydb3.close()
            response = app.response_class(json.dumps(
                signup_fail, ensure_ascii=False), status=400, mimetype='application/json')
            return response
        elif not name.isalnum() or not password.isalnum():
            signup_fail = {
                "error": True,
                "message": "帳號及密碼請填寫字母或數字"
            }
            mydb3.close()
            response = app.response_class(json.dumps(
                signup_fail, ensure_ascii=False), status=400, mimetype='application/json')
            return response
        else:
            sql = "INSERT INTO signup (username, email, password) VALUES (%s,%s,%s) "
            val = (name, email, password)
            mycursor.execute(sql, val)
            mydb3.commit()

            signup_success = {
                "ok": True,
                "message": "註冊成功，請登入系統"
            }

            mydb3.close()
            response = app.response_class(json.dumps(
                signup_success, ensure_ascii=False), status=200, mimetype='application/json')
            return response

    except Error as error:
        signup_fail = {
            "error": True,
            "message": "Email 已經註冊帳戶"
        }
        response = app.response_class(json.dumps(
            signup_fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/user", methods=["PATCH"])
def signin():
    try:
        mydb4 = mysql.connector.connect(pool_name="mypool")
        mycursor = mydb4.cursor()
        data = request.get_json(force=True)
        email = data['email']
        password = data['password']
        if email == "" or password == "":
            signin_fail = {
                "error": True,
                "message": "請輸入會員帳號密碼資料"
            }
            mydb4.close()
            response = app.response_class(json.dumps(
                signin_fail, ensure_ascii=False), status=200, mimetype='application/json')
            return response

        else:
            mydb4 = mysql.connector.connect(pool_name="mypool")
            mycursor = mydb4.cursor()
            sql = "SELECT * FROM signup WHERE email = %s and password = %s"
            val = (email, password)
            mycursor.execute(sql, val)
            record = mycursor.fetchone()
            if record != None:
                signin_success = {
                    "ok": True
                }

                session['status'] = 'login'
                session['userid'] = record[0]
                session['username'] = record[1]
                session['email'] = record[2]

                mydb4.close()
                response = app.response_class(json.dumps(
                    signin_success, ensure_ascii=False), status=200, mimetype='application/json')
                return response
            else:
                signin_fail = {
                    "error": True,
                    "message": "電子郵件或密碼錯誤"
                }

                session['status'] = 'unlogin'
                mydb4.close()
                response = app.response_class(json.dumps(
                    signin_fail, ensure_ascii=False), status=400, mimetype='application/json')
                return response

    except Error as error:
        signin_fail = {
            "error": True,
            "message": "帳號已經被註冊"
        }
        mydb4.close()
        response = app.response_class(json.dumps(
            signin_fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/user", methods=["DELETE"])
def signout():
    session['status'] = 'unlogin'
    signout_success = {
        "ok": True,
    }
    response = app.response_class(json.dumps(
        signout_success, ensure_ascii=False), status=200, mimetype='application/json')
    return response


@app.route("/api/booking", methods=["GET"])
def inbooking():
    try:
        if session['status'] == 'login':
            mydb5 = mysql.connector.connect(pool_name="mypool")
            mycursor = mydb5.cursor()
            sql = "SELECT * FROM booking"
            mycursor.execute(sql)
            record = mycursor.fetchall()
            if record != []:
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
                mydb5.close()
                response = app.response_class(json.dumps(
                    booking_data, ensure_ascii=False), status=200, mimetype='application/json')
                return response
            else:
                null = None
                booking_data = {"data": null}
                mydb5.close()
                response = app.response_class(json.dumps(
                    booking_data, ensure_ascii=False), status=200, mimetype='application/json')
                return response
    except Error as error:
        booking_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
        response = app.response_class(json.dumps(
            booking_fail, ensure_ascii=False), status=403, mimetype='application/json')
        return response


@app.route("/api/booking", methods=["POST"])
def booked():
    data = request.get_json(force=True)
    attractionId = data['attractionId']
    date = data['date']
    datenow = data['datenow']
    time = data['time']
    price = data['price']

    try:
        status = session.get('status')
        if status == 'login':
            mydb6 = mysql.connector.connect(pool_name="mypool")
            mycursor = mydb6.cursor()
            if mydb6.is_connected():
                if date == "" or datenow > date:
                    booking_fail = {
                        "error": True,
                        "message": "未選擇日期或輸入過去的日期"
                    }
                    mydb6.close()
                    response = app.response_class(json.dumps(
                        booking_fail, ensure_ascii=False), status=400, mimetype='application/json')
                    return response
                else:
                    sql = "INSERT INTO booking (attractionId, date, time, price) VALUES (%s,%s,%s,%s)"
                    val = (attractionId, date, time, price)
                    mycursor.execute(sql, val)
                    mydb6.commit()
                    booking_success = {
                        "ok": True,
                    }
                    session['date'] = date
                    session['time'] = time
                    session['price'] = price

                    mydb6.close()
                    response = app.response_class(json.dumps(
                        booking_success, ensure_ascii=False), status=200, mimetype='application/json')
                    return response
            else:
                booking_fail = {
                    "error": True,
                    "message": "建立失敗，輸入不正確或其他原因"
                }
                mydb6.close()
                response = app.response_class(json.dumps(
                    booking_fail, ensure_ascii=False), status=400, mimetype='application/json')
                return response
        else:
            booking_fail = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            response = app.response_class(json.dumps(
                booking_fail, ensure_ascii=False), status=403, mimetype='application/json')
            return response
    except Error as error:
        booking_fail = {
            "error": True,
            "message": "請填寫行程資料"
        }
        response = app.response_class(json.dumps(
            booking_fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/booking", methods=["DELETE"])
def delBooked():
    status = session.get('status')
    if status == "login":
        mydb7 = mysql.connector.connect(pool_name="mypool")
        mycursor = mydb7.cursor()
        if mydb7.is_connected():
            sql = "DELETE from booking"
            mycursor.execute(sql)
            mydb7.commit()

            del_success = {
                "ok": True,
            }
            mydb7.close()
            response = app.response_class(json.dumps(
                del_success, ensure_ascii=False), status=200, mimetype='application/json')
            return response
        else:
            del_fail = {
                "error": True,
                "message": "資料刪除失敗"
            }
            mydb7.close()
            response = app.response_class(json.dumps(
                del_fail, ensure_ascii=False), status=400, mimetype='application/json')
            return response
    else:
        del_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
        response = app.response_class(json.dumps(
            del_fail, ensure_ascii=False), status=403, mimetype='application/json')
        return response


@app.route("/api/orders", methods=["POST"])
def order():
    try:
        status = session.get('status')
        if status == 'login':
            data = request.get_json(force=True)
            prime = data['prime']

            session['order'] = "unpaid"
            session['contact_name'] = data['order']['contact']['name']
            session['contact_email'] = data['order']['contact']['email']
            session['contact_phone'] = data['order']['contact']['phone']

            if session['contact_name'] == "" or session['contact_email'] == "" or session['contact_phone'] == "":
                order_fail = {
                    "error": True,
                    "message": "訂單建立失敗，未輸入資料"
                }

                response = app.response_class(json.dumps(
                    order_fail, ensure_ascii=False), status=400, mimetype='application/json')
                return response
            elif not session['contact_name'].isalnum() or not session['contact_phone'].isalnum() or not session['contact_phone'].isnumeric():
                order_fail = {
                    "error": True,
                    "message": "訂單建立失敗，輸入不正確"
                }

                response = app.response_class(json.dumps(
                    order_fail, ensure_ascii=False), status=400, mimetype='application/json')
                return response
            else:
                load_dotenv()
                url = "https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime"
                headers = {'content-type': 'application/json',
                           'x-api-key': 'partner_D7xWITe3QnKxgA4p6ZIJrvkKLzyAkdRybJQeIw3RZKvjtgDnLSHjdxRu'}
                data = {
                    "prime": prime,
                    "partner_key": os.getenv('PARTNER_KEY'),
                    "merchant_id": "Chiao_ESUN",
                    "details": "TapPay Test",
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

                req = requests.post(
                    url, data=json.dumps(data), headers=headers)
                result = json.loads(req.text)

                if result['status'] == 0:
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

                    response = app.response_class(json.dumps(
                        pay_success, ensure_ascii=False), status=200, mimetype='application/json')
                    return response
                else:
                    pay_fail = {
                        "data": {
                            "number": result['rec_trade_id'],
                            "payment": {
                                "status": 1,
                                "message": "付款失敗"
                            }
                        }
                    }

                    response = app.response_class(json.dumps(
                        pay_fail, ensure_ascii=False), status=200, mimetype='application/json')
                    return response
        else:
            order_fail = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            response = app.response_class(json.dumps(
                order_fail, ensure_ascii=False), status=403, mimetype='application/json')
            return response
    except Error as error:
        order_fail = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        response = app.response_class(json.dumps(
            order_fail, ensure_ascii=False), status=500, mimetype='application/json')
        return response


@app.route("/api/order/<orderNumber>")
def orderId(orderNumber):
    status = session.get('status')
    if status == 'login':
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
            },
            "message": "已發送確認信件拉! 去看看你的信箱吧 :)"
        }

        load_dotenv()
        msg = Message('恭喜完成預定台北一日遊行程', sender=str(
            os.getenv('EMAIL')), recipients=[session['contact_email']])
        msg.html = render_template("email.html", number=orderNumber, price=session['price'], name=session['name'], address=session[
                                   'address'], image=session['image'][0], date=session['date'], time=session['time'], username=session['contact_name'])
        mail.send(msg)

        response = app.response_class(json.dumps(
            orderinfo, ensure_ascii=False), status=200, mimetype='application/json')
        return response
    else:
        order_fail = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
        response = app.response_class(json.dumps(
            order_fail, ensure_ascii=False), status=403, mimetype='application/json')
        return response


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
