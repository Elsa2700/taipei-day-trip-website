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
                                    let footer_del_text = document.createElement("div");
                                    footer_del_text.className = "footer_del_text";
                                    footer_del_text.textContent = "COPYRIGHT © 2021 台北一日遊";
                                    document.getElementById("footer").style.display = "none";
                                    footer_frame.appendChild(footer_del).appendChild(footer_del_text);

                                } else {
                                    console.log(dataobj.data.length)
                                    console.log(dataobj.data)

                                    for (let i = 0; i < dataobj.data.length; i++) {
                                        //框架
                                        let item_group = document.getElementById("booking-frame");
                                        let item = document.createElement("div");
                                        item.className = "section";

                                        //圖片
                                        let del_img = document.createElement("img");
                                        del_img.src = "/static/css/icon_delete.png";
                                        del_img.className = "del";
                                        del_img.id = "del" + i;
                                        item_group.appendChild(item).appendChild(del_img);

                                        let pic = document.createElement("div");
                                        pic.className = "pic"
                                        let pic_f = document.createElement("div");
                                        pic_f.className = "pic-frame"
                                        let pic_img = document.createElement("img");
                                        pic_img.src = dataobj.data[i]["attraction"]["image"];
                                        pic_img.className = "attracion-pic";
                                        pic_img.id = "attracion-pic";
                                        item_group.appendChild(item).appendChild(pic).appendChild(pic_f).appendChild(pic_img);

                                        let item_b = document.createElement("div");
                                        item_b.className = "booking";
                                        let item_b_f = document.createElement("div");
                                        item_b_f.className = "booking-frame";
                                        item_b_f.id = "booking-frame";
                                        //景點名稱
                                        let b_t = document.createElement("h2");
                                        b_t.className = "booking-title";
                                        b_t.textContent = "台北一日遊：";
                                        let b_t_name = document.createElement("span");
                                        b_t_name.className = "booking-title";
                                        b_t_name.textContent = dataobj.data[i]["attraction"]["name"];
                                        item_group.appendChild(item).appendChild(item_b).appendChild(item_b_f).appendChild(b_t).appendChild(b_t_name);


                                        let b_c = document.createElement("div");
                                        b_c.className = "booking-content";
                                        //景點日期
                                        let b_c_t_d = document.createElement("div");
                                        b_c_t_d.className = "b-c-title";
                                        b_c_t_d.textContent = "日期：";
                                        let b_c_date = document.createElement("span");
                                        b_c_date.className = "b-c-content";
                                        b_c_date.textContent = dataobj.data[i]["date"];
                                        item_group.appendChild(item).appendChild(item_b).appendChild(item_b_f).appendChild(b_c).appendChild(b_c_t_d).appendChild(b_c_date);

                                        //景點時間
                                        let b_c_t_t = document.createElement("div");
                                        b_c_t_t.className = "b-c-title";
                                        b_c_t_t.textContent = "時間：";
                                        let b_c_time = document.createElement("span");
                                        b_c_time.className = "b-c-content";
                                        b_c_time.textContent = dataobj.data[i]["time"];
                                        item_group.appendChild(item).appendChild(item_b).appendChild(item_b_f).appendChild(b_c).appendChild(b_c_t_t).appendChild(b_c_time);


                                        //景點費用
                                        let b_c_t_p = document.createElement("div");
                                        b_c_t_p.className = "b-c-title";
                                        b_c_t_p.textContent = "費用：";
                                        let b_c_price = document.createElement("span");
                                        b_c_price.className = "b-c-content";
                                        b_c_price.textContent = "新台幣" + dataobj.data[i]["price"] + "元";
                                        item_group.appendChild(item).appendChild(item_b).appendChild(item_b_f).appendChild(b_c).appendChild(b_c_t_p).appendChild(b_c_price);

                                        //景點地點
                                        let b_c_t_pl = document.createElement("div");
                                        b_c_t_pl.className = "b-c-title";
                                        b_c_t_pl.textContent = "地點：";
                                        let b_c_ads = document.createElement("span");
                                        b_c_ads.className = "b-c-content";
                                        b_c_ads.textContent = dataobj.data[i]["attraction"]["address"];
                                        item_group.appendChild(item).appendChild(item_b).appendChild(item_b_f).appendChild(b_c).appendChild(b_c_t_pl).appendChild(b_c_ads);


                                    }


                                    //點擊刪除預定行程內容========

                                    let delimg = document.querySelectorAll(".del");
                                    console.log(delimg.length);
                                    for (let i = 0; i < delimg.length; i++) {
                                        // 事件處理:取得指定訂單的ID
                                        delimg[i].addEventListener("mouseover", getId);
                                        function getId(e) {
                                            del_id = e.target.id;
                                            console.log(del_id);
                                            let delimg_id = document.getElementById(del_id);
                                            // 事件處理:點擊刪除訂單的ID
                                            delimg_id.addEventListener("click", del);

                                            function del(e) {
                                                console.log("刪除行程")
                                                e.preventDefault;
                                                let data = {
                                                    "number": i
                                                }
                                                let options = {
                                                    method: 'DELETE',
                                                    headers: {
                                                        'Content-Type': 'application/json',
                                                    },
                                                    body: JSON.stringify(data)
                                                };
                                                console.log(options);
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

                                    }




                                }
                            })

                    }

                }
            })
    }
}