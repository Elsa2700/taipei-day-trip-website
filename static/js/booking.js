function getData() {
    //載入頁面，檢查使用者狀態
    querybookingState();

    async function querybookingState() {
        await fetch("/api/user")
            .then(res => {
                console.log(res);
                return res.json();
            })
            .then(result => {
                let dataobj = result;


                if (dataobj["data"] == null) {
                    //判斷式:null(未登入):導向首頁
                    window.location.href = "/";

                } else {
                    //判斷式:不為null(已登入)
                    console.log("登入狀態")
                    username = dataobj["data"]["name"]

                    // 導覽頁畫面呈現登入狀態
                    //判斷式:非null
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

                        async function signoutReq() {
                            await fetch('/api/user', options)
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


                        }
                    }

                    //顯示預訂行程畫面
                    queryinBooking(username);
                    async function queryinBooking(username) {
                        await fetch("/api/booking")
                            .then(res => {
                                return res.json();
                            })
                            .then(content => {
                                let dataobj = content;
                                //歡迎會員標頭說明
                                let b_user = document.getElementById("username_booking");
                                b_user.textContent = username;
                                

                                //行程訂單:有訂單、無訂單
                                if (dataobj["data"] == null) {
                                    console.log('刪除資料')
                                    //無任何行程訂單
                                    let footer_frame = document.getElementById("footer_frame")
                                    let bookingframe = document.getElementById("frame_scene");
                                    bookingframe.innerHTML = "";
                                    bookingframe.textContent = "目前沒有任何待預訂的行程";
                                    // //產生footer 標籤
                                    let footer_del = document.createElement("div");
                                    footer_del.className = "footer_del";
                                    let footer_del_text =document.createElement("div");
                                    footer_del_text.className ="footer_del_text";
                                    footer_del_text.textContent ="COPYRIGHT © 2021 台北一日遊";
                                    document.getElementById("footer").style.display = "none";
                                    footer_frame.appendChild(footer_del).appendChild(footer_del_text);

                                } else {
                                    //圖片
                                    let attracion_pic = document.getElementById("attracion-pic");
                                    attracion_pic.src = dataobj.data["attraction"]["image"][0];
                                    //景點名稱
                                    let profile_name = document.getElementById("b-t-name");
                                    profile_name.textContent = dataobj.data["attraction"]["name"];
                                    //景點日期
                                    let profile_date = document.getElementById("b-c-date");
                                    profile_date.textContent = dataobj.data["date"];
                                    //景點時間
                                    let profile_time = document.getElementById("b-c-time");
                                    profile_time.textContent = dataobj.data["time"];
                                    //景點費用
                                    let profile_price = document.getElementById("b-c-price");
                                    profile_price.textContent = dataobj.data["price"];
                                    //景點地點
                                    let profile_ads = document.getElementById("b-c-ads");
                                    profile_ads.textContent = dataobj.data["attraction"]["address"];
                                }
                            })

                    }
                    //點擊刪除預定行程內容
                    let delimg = document.getElementById("del");
                    delimg.addEventListener("click", del);
                    
                    function del(e) {
                        console.log("刪除行程")
                        e.preventDefault;
                        let options = {
                            method: 'DELETE',
                            headers: {
                                'Content-Type': 'application/json',
                            },
                        };

                        delReq('/api/booking', options);

                        async function delReq() {
                            await fetch('/api/booking', options)
                                .then(res => {
                                    console.log(res);
                                    return res.json();
                                })
                                .then(result => {
                                    let dataobj = result;
                                    console.log(dataobj);
                                    //重新載入頁面
                                    window.document.location.reload();
                                })


                        }



                    }
                }
            })
    }
}