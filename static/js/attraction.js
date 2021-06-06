
//取得景點api資訊
let href = location.href;
let id = href.split('/')[4];
let url = "/api/attraction/" + id;

queryId(url);
function queryId(url) {
    // 載入畫面
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "block"
    };
    fetch(url)
        .then(res => {
            return res.json();
        })
        .then(content => {
            let dataobj = content;
            //景點名稱
            let profile_title = document.getElementById("profile-title");
            profile_title.textContent = dataobj.data["name"];
            //景點類別
            let profile_content = document.getElementById("profile-content");
            profile_content.textContent = dataobj.data["category"] + " at " + dataobj.data["mrt"];
            //資訊
            let info_content = document.getElementById("info-content");
            info_content.textContent = dataobj.data["description"];
            //地址
            let ads_content = document.getElementById("ads-content");
            ads_content.textContent = dataobj.data["address"];
            //交通
            let trf_content = document.getElementById("trf-content");
            trf_content.textContent = dataobj.data["transport"];
            //圖片
            let attracion_pic = document.getElementById("attracion-pic");
            attracion_pic.src = dataobj.data["images"][0];
            let index = 0;
            let imglen = dataobj.data["images"].length;

            //價格
            let field_price = document.getElementById("field-price");
            field_price.textContent = "新台幣 2000 元";


            //小圓點
            let btn_circle = document.getElementById("btn-circle");
            for (let i = 0; i < imglen; i++) {
                let img_circle = document.createElement("img");
                img_circle.id = "img_circle" + i;
                img_circle.src = "/static/css/circle_current.png";
                btn_circle.appendChild(img_circle);
            }


            //箭頭事件處理器
            let btn_left = document.getElementById("btn-left");
            btn_left.addEventListener("click", left);
            let btn_right = document.getElementById("btn-right");
            btn_right.addEventListener("click", right);

            //點擊左箭頭
            function left() {
                console.log("左" + index);
                index--;
                if (index < 0) {
                    index = imglen - Math.abs(index);
                }
                attracion_pic.src = dataobj.data["images"][index];
                let img_circle_index = document.getElementById("img_circle" + index);
                let img_circle = document.getElementById("img_circle*");
                for (let i = 0; i < imglen; i++) {
                    if (("img_circle" + i) == img_circle_index.id) {
                        console.log(("img_circle" + i));
                        console.log(img_circle_index.id);
                        document.getElementById("img_circle" + i).src = "/static/css/circle_current_b.png";
                    } else {
                        document.getElementById("img_circle" + i).src = "/static/css/circle_current.png";
                    }
                }
<<<<<<< HEAD

                // 使用者登入、註冊設定========================
                // 登入視窗=================================================
                let loginId = document.getElementById("loginId");
                loginId.addEventListener("click", Login);
                function Login() {
                    document.getElementById("loginPage").style.display = "block";
                }

                // 轉至註冊視窗(點擊)=================================================
                let signupPage = document.getElementById("msg-signup");
                signupPage.addEventListener("click", querySignup);
                function querySignup() {
                    document.getElementById("signupPage").style.display = "block";
                    console.log("轉至登入視窗")

                }
                // 轉至登入視窗(點擊)=================================================
                let loginPage = document.getElementById("msg-login");
                loginPage.addEventListener("click", queryLogin);
                function queryLogin() {
                    document.getElementById("signupPage").style.display = "none";
=======
            }
            //點擊左箭頭

            function right(e) {
                e.preventDefault();
                console.log("右" + index);
                index++;
                if (index >= imglen) {
                    index = index % imglen;
                }
                attracion_pic.src = dataobj.data["images"][index];
                let img_circle_index = document.getElementById("img_circle" + index);
                let img_circle = document.getElementById("img_circle*");
                for (let i = 0; i < imglen; i++) {
                    if (("img_circle" + i) == img_circle_index.id) {
                        console.log(("img_circle" + i));
                        console.log(img_circle_index.id);
                        document.getElementById("img_circle" + i).src = "/static/css/circle_current_b.png";
                    } else {
                        document.getElementById("img_circle" + i).src = "/static/css/circle_current.png";
                    }
                }

            }

            // 使用者登入、註冊設定========================
            // 登入視窗=================================================
            let loginId = document.getElementById("loginId");
            loginId.addEventListener("click", Login);
            function Login() {
                document.getElementById("loginPage").style.display = "block";
            }

            // 轉至註冊視窗(點擊)=================================================
            let signupPage = document.getElementById("msg-signup");
            signupPage.addEventListener("click", querySignup);
            function querySignup() {
                document.getElementById("signupPage").style.display = "block";
                console.log("轉至登入視窗")

            }
            // 轉至登入視窗(點擊)=================================================
            let loginPage = document.getElementById("msg-login");
            loginPage.addEventListener("click", queryLogin);
            function queryLogin() {
                document.getElementById("signupPage").style.display = "none";

            }
            //註冊(送出)================================================
            let signup_btn = document.getElementById("signup-btn");
            signup_btn.addEventListener("click", submitSignup);
            function submitSignup(e) {
                //抓取註冊資訊
                let username = document.getElementById("signup-username").value;
                let email = document.getElementById("signup-email").value;
                let psd = document.getElementById("signup-psd").value;

                //request body
                let data = {
                    "name": username,
                    "email": email,
                    "password": psd
                };

                let options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                };
                console.log(options);

                e.preventDefault();


                signupReq('/api/user', options)

                function signupReq() {

                    fetch('/api/user', options)
                        .then(res => {
                            console.log(res);
                            return res.json();
                        })
                        .then(result => {
                            let dataobj = result;
                            console.log(dataobj["error"])
                            if (dataobj["error"] == true) {
                                let text = document.querySelector("#signup-msg")
                                text.textContent = dataobj["message"];
                                text.style.color = "red";

                            } else {
                                let text = document.querySelector("#signup-msg")
                                text.textContent = "註冊成功，請登入系統";
                                text.style.color = "green";
                            }

                        })
                        .catch(error => {
                            console.error("更新失敗");
                            let text = document.querySelector("#signup-msg")
                            text.textContent = "請輸入會員帳號密碼";
                            text.style.color = "red";
                        })
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a

                }

<<<<<<< HEAD
                            })
                            .catch(error => {
                                console.error("更新失敗");
                                let text = document.querySelector("#signup-msg")
                                text.textContent = "請輸入會員帳號密碼";
                                text.style.color = "red";
                            })
=======
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a


            }

            //登入(送出)================================================
            let signin_btn = document.getElementById("signin-btn");
            signin_btn.addEventListener("click", submitSignin);
            function submitSignin(e) {

                //抓取登入資訊
                let email = document.getElementById("signin-email").value;
                let psd = document.getElementById("signin-psd").value;

<<<<<<< HEAD
                //登入(送出)================================================
                let signin_btn = document.getElementById("signin-btn");
                signin_btn.addEventListener("click", submitSignin);
                function submitSignin(e) {

                    //抓取登入資訊
                    let email = document.getElementById("signin-email").value;
                    let psd = document.getElementById("signin-psd").value;

                    //request body
                    let data = {
                        "email": email,
                        "password": psd
                    };

                    let options = {
                        method: 'PATCH',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify(data)
                    };
                    console.log(options);

                    e.preventDefault();


                    signinReq('/api/user', options)

                    async function signinReq() {
                        await fetch('/api/user', options)
                            .then(res => {
                                console.log(res);
                                return res.json();
                            })
                            .then(result => {
                                console.log(result["error"])
                                if (result["error"] == true) {
                                    let text = document.querySelector("#signin-msg");
                                    text.textContent = result["message"];
                                    text.style.color = "red";
                                } else {
                                    //重新載入頁面
                                    window.document.location.reload();
                                }

                            })
                            .catch(error => {
                                console.error("更新失敗");
                                let text = document.querySelector("#signin-msg")
                                text.textContent = "請輸入會員帳號密碼";
                                text.style.color = "red";
                            })
=======
                //request body
                let data = {
                    "email": email,
                    "password": psd
                };

                let options = {
                    method: 'PATCH',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(data)
                };
                console.log(options);
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a

                e.preventDefault();


                signinReq('/api/user', options)

<<<<<<< HEAD
                }

                // 關閉登入視窗(外層)=================================================    
                let outerPagelogin = document.getElementById("login-bgPage");
                outerPagelogin.addEventListener("click", loginClose);
                function loginClose() {
                    document.getElementById("loginPage").style.display = "none";
                    console.log("關閉視窗")

                }
                let outerPagesignup = document.getElementById("signup-bgPage");
                outerPagesignup.addEventListener("click", signupClose);
                function signupClose() {
                    document.getElementById("signupPage").style.display = "none";
                    document.getElementById("loginPage").style.display = "none";

                }

                // 關閉登入視窗(內層固定)=================================================    
                let innerPage_login = document.getElementById("loginPage-frame")
                let innerPage_signup = document.getElementById("signupPage-frame")
                innerPage_login.addEventListener("click", open);
                innerPage_signup.addEventListener("click", open);
                function open(e) {
                    document.getElementById("loginPage").style.display = "block";
                    e.stopPropagation();
                    e.preventDefault();
                }
                // 關閉登入視窗(內層關閉)=================================================  
                let closeLogin = document.getElementById("close-login");
                closeLogin.addEventListener("click", CloseLogin);
                function CloseLogin(e) {
                    document.getElementById("loginPage").style.display = "none";
                    e.stopPropagation();
                }

                let closeSignup = document.getElementById("close-signup");
                closeSignup.addEventListener("click", CloseSignup);
                function CloseSignup(e) {
                    document.getElementById("signupPage").style.display = "none";
                    document.getElementById("loginPage").style.display = "none";
                    e.stopPropagation();
                }

                //當前使用者登入狀態=========================================
                queryState();
                async function queryState() {
                    await fetch("/api/user")
=======
                function signinReq() {
                    fetch('/api/user', options)
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a
                        .then(res => {
                            console.log(res);
                            return res.json();
                        })
                        .then(result => {
                            console.log(result["error"])
                            if (result["error"] == true) {
                                let text = document.querySelector("#signin-msg");
                                text.textContent = result["message"];
                                text.style.color = "red";
                            } else {
                                //重新載入頁面
                                window.document.location.reload();
                            }

<<<<<<< HEAD
                            if (dataobj["data"] == null) {
                                //判斷式:null(未登入)
                                let text = document.querySelector("#logintext");
                                text.textContent = "登入/註冊";

                            } else {
                                //判斷式:非null(已登入)
                                let text = document.querySelector("#logintext");
                                text.textContent = "登出系統";
                                //登出(點擊)
                                text.addEventListener("click", signout);
                                function signout(e) {
                                    e.preventDefault;
                                    let options = {
                                        method: 'DELETE',
                                        headers: {
                                            'Content-Type': 'application/json',
                                        },
                                    };
                                    signoutReq('/api/user', options);
=======
                        })
                        .catch(error => {
                            console.error("更新失敗");
                            let text = document.querySelector("#signin-msg")
                            text.textContent = "請輸入會員帳號密碼";
                            text.style.color = "red";
                        })

                }

>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a


            }

            // 關閉登入視窗(外層)=================================================    
            let outerPagelogin = document.getElementById("login-bgPage");
            outerPagelogin.addEventListener("click", loginClose);
            function loginClose() {
                document.getElementById("loginPage").style.display = "none";
                console.log("關閉視窗")

            }
            let outerPagesignup = document.getElementById("signup-bgPage");
            outerPagesignup.addEventListener("click", signupClose);
            function signupClose() {
                document.getElementById("signupPage").style.display = "none";
                document.getElementById("loginPage").style.display = "none";

            }

            // 關閉登入視窗(內層固定)=================================================    
            let innerPage_login = document.getElementById("loginPage-frame")
            let innerPage_signup = document.getElementById("signupPage-frame")
            innerPage_login.addEventListener("click", open);
            innerPage_signup.addEventListener("click", open);
            function open(e) {
                document.getElementById("loginPage").style.display = "block";
                e.stopPropagation();
                e.preventDefault();
            }
            // 關閉登入視窗(內層關閉)=================================================  
            let closeLogin = document.getElementById("close-login");
            closeLogin.addEventListener("click", CloseLogin);
            function CloseLogin(e) {
                document.getElementById("loginPage").style.display = "none";
                e.stopPropagation();
            }

            let closeSignup = document.getElementById("close-signup");
            closeSignup.addEventListener("click", CloseSignup);
            function CloseSignup(e) {
                document.getElementById("signupPage").style.display = "none";
                document.getElementById("loginPage").style.display = "none";
                e.stopPropagation();
            }

            //當前使用者登入狀態=========================================
            queryState();
            function queryState() {
                // 載入畫面
                window.onload = function () {
                    let load = document.getElementById("load");
                    load.style.display = "block"
                };
                fetch("/api/user")
                    .then(res => {
                        console.log(res);
                        return res.json();
                    })
                    .then(result => {
                        let dataobj = result;
                        console.log(dataobj["data"])

                        if (dataobj["data"] == null) {
                            //判斷式:null(未登入)
                            let text = document.querySelector("#logintext");
                            text.textContent = "登入/註冊";

                        } else {
                            //判斷式:非null(已登入)
                            let text = document.querySelector("#logintext");
                            text.textContent = "登出系統";
                            //登出(點擊)
                            text.addEventListener("click", signout);
                            function signout(e) {
                                e.preventDefault;
                                let options = {
                                    method: 'DELETE',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                };
                                signoutReq('/api/user', options);

                                function signoutReq() {
                                    // 載入畫面
                                    window.onload = function () {
                                        let load = document.getElementById("load");
                                        load.style.display = "block"
                                    };
                                    fetch('/api/user', options)
                                        .then(res => {
                                            console.log(res);
                                            return res.json();
                                        })
                                        .then(result => {
                                            let dataobj = result;
                                            if (dataobj["ok"] == true) {
                                                //重新載入頁面
                                                window.document.location.reload();
                                            }
                                        })

<<<<<<< HEAD
=======

                                }
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a
                            }

                        }



                    })
                // 結束畫面
                window.onload = function () {
                    let load = document.getElementById("load");
                    load.style.display = "none"
                };
            }

<<<<<<< HEAD


            })
    }
=======
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a



        })
    // 結束畫面
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "none"
    };
}

//訂購按鈕畫面
let time_api = "早上 9 點到下午 4 點";
let price_api = "2000";
function radioText(e) {
    let field_price = document.getElementById("field-price");
    let price = document.querySelector('input[name="notaswitch-two"]:checked').value
    field_price.textContent = price;
    time_api = e.id;
    if (time_api == "morning") {
        time_api = "早上 9 點到下午 4 點"
    } else {
        time_api = "下午 2 點到晚上 9 點"
    }
    price_api = e.value.substr(3, 5);

}


//開始預定行程
let booking = document.getElementById("booking");
booking.addEventListener("click", queryBooking);
function queryBooking() {
    querybookingState();
    function querybookingState() {
        // 載入畫面
        window.onload = function () {
            let load = document.getElementById("load");
            load.style.display = "block"
        };
        fetch("/api/user")
            .then(res => {
                console.log(res);
                return res.json();
            })
            .then(result => {
                let dataobj = result;
                console.log(dataobj["data"])

                if (dataobj["data"] == null) {
                    //判斷式:null(未登入)
                    Login();
                } else {
                    window.location.href = "/booking";

                }


            })
        // 結束畫面
        window.onload = function () {
            let load = document.getElementById("load");
            load.style.display = "none"
        };

    }
<<<<<<< HEAD
    let start_booking = document.getElementById("start-booking");
    start_booking.addEventListener("click", queryinBooking);
    function queryinBooking() {
        querybookingState();
        async function querybookingState() {
            await fetch("/api/user")
                .then(res => {
                    console.log(res);
                    return res.json();
                })
                .then(result => {
                    let dataobj = result;
                    console.log(dataobj["data"])

                    if (dataobj["data"] == null) {
                        //判斷式:null(未登入)
                        Login();
                        function Login() {
                            document.getElementById("loginPage").style.display = "block";
                        }
                    } else {
                        //判斷式:不為null(已登入)
                        newBooking()
                        function newBooking(e) {
                            //抓取註冊資訊
                            let now = new Date();
                            let today = now.getFullYear() + "-" +(now.getMonth()+1).toString().padStart(2, "0") + "-" + now.getDate().toString().padStart(2, "0");
                            let date_api = document.getElementById("date").value;
                            // console.log("現在",today);
                            // console.log("預定日",date_api);
                            // console.log(date_api > today);

                            //request body
                            let data = {
                                "attractionId": id,
                                "date": date_api,
                                "datenow": today,
                                "time": time_api,
                                "price": price_api
                            };
=======
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a


}
let start_booking = document.getElementById("start-booking");
start_booking.addEventListener("click", queryinBooking);
function queryinBooking() {
    querybookingState();
    function querybookingState() {
        // 載入畫面
        window.onload = function () {
            let load = document.getElementById("load");
            load.style.display = "block"
        };
        fetch("/api/user")
            .then(res => {
                console.log(res);
                return res.json();
            })
            .then(result => {
                let dataobj = result;
                console.log(dataobj["data"])

                if (dataobj["data"] == null) {
                    //判斷式:null(未登入)
                    Login();
                    function Login() {
                        document.getElementById("loginPage").style.display = "block";
                    }
                } else {
                    //判斷式:不為null(已登入)
                    newBooking()
                    function newBooking(e) {
                        //抓取註冊資訊
                        let now = new Date();
                        let today = now.getFullYear() + "-" + (now.getMonth() + 1).toString().padStart(2, "0") + "-" + now.getDate().toString().padStart(2, "0");
                        let date_api = document.getElementById("date").value;
                        // console.log("現在",today);
                        // console.log("預定日",date_api);
                        // console.log(date_api > today);

                        //request body
                        let data = {
                            "attractionId": id,
                            "date": date_api,
                            "datenow": today,
                            "time": time_api,
                            "price": price_api
                        };

                        let options = {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                            body: JSON.stringify(data)
                        };
                        console.log(options);

                        //向後端連線取得booking api回應
                        bookingReq('/api/booking', options)

                        function bookingReq() {
                            // 載入畫面
                            window.onload = function () {
                                let load = document.getElementById("load");
                                load.style.display = "block"
                            };
<<<<<<< HEAD
                            console.log(options);

                            //向後端連線取得booking api回應
                            bookingReq('/api/booking', options)

                            async function bookingReq() {
                                await fetch('/api/booking', options)
                                    .then(res => {
                                        console.log(res);
                                        return res.json();
                                    })
                                    .then(result => {
                                        if (result["error"] == true) {
                                            let text = document.querySelector("#msg")
                                            text.textContent = result["message"];
                                            text.style.color = "red";

                                        } else {
                                            let text = document.querySelector("#msg")
                                            text.textContent = "成功建立行程";
                                            text.style.color = "green";
                                            window.location.href = "/booking";
                                        }

                                    })
                                    .catch(error => {
                                        console.error("更新失敗");
=======
                            fetch('/api/booking', options)
                                .then(res => {
                                    console.log(res);
                                    return res.json();
                                })
                                .then(result => {
                                    if (result["error"] == true) {
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a
                                        let text = document.querySelector("#msg")
                                        text.textContent = result["message"];
                                        text.style.color = "red";

                                    } else {
                                        let text = document.querySelector("#msg")
                                        text.textContent = "成功建立行程";
                                        text.style.color = "green";
                                        window.location.href = "/booking";
                                    }

                                })
                                .catch(error => {
                                    console.error("更新失敗");
                                    let text = document.querySelector("#msg")
                                    text.textContent = "更新失敗";
                                })

                        }



                    }



                }


            })
        // 結束畫面
        window.onload = function () {
            let load = document.getElementById("load");
            load.style.display = "none"
        };

    }
}








