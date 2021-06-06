
//定義變數==================================================

//取得關鍵字
let keyword = document.getElementById("keyword").value;
//預設頁碼
let page = 0;


//定義各種url==================================================

// 串接首頁路由: 定義url
if (keyword != "") {
    const url = `/api/attractions?page=${page}&keyword=${keyword}`;
    if (page != null) {
        queryAttraction(page, keyword, url);
    } else {
        console.log("無資料");
    }

} else {
    let url = `/api/attractions?page=${page}`;
    if (page != null) {
        queryImg(page, url);
    } else {
        console.log("無資料");
    }
}

// 有圖片、無關鍵字
function queryImg(page, url) {
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
            let item_group = document.querySelector("#attractions-group");

            for (let i = 0; i < dataobj.data.length; i++) {
                //框架

                let item = document.createElement("div");
                item.className = "attraction-desktop";

                //取得景點編號
                function clickId(e) {
                    e.preventDefault();
                    id = this.getAttribute('id');
                    let url_id = "/attraction/" + id;
                    window.location.href = url_id;
                }

                //景點編號
                item.id = dataobj.data[i]["id"];
                item.addEventListener("click", clickId);



                //圖片

                let url_img = dataobj.data[i]["images"][0];
                let image = new Image();
                image.src = url_img
                image.className = "img";
                item_group.appendChild(item).appendChild(image);

                //文字
                let title_text = dataobj.data[i]["name"];
                if (title_text != null) {
                    title_text.className = "title";
                    let title_text_tag = document.createElement("div");
                    title_text_tag.className = "title";
                    title_text_tag.textContent = title_text;
                    item_group.appendChild(item).appendChild(title_text_tag);
                }

                let text = document.createElement("div");
                text.className = "text_attraction";
                text.id = "text";
                let cat_text = dataobj.data[i]["category"];
                if (cat_text != null) {
                    cat_text.className = "cat";
                    let cat_text_tag = document.createElement("div");
                    cat_text_tag.className = "cat";
                    cat_text_tag.textContent = cat_text;
                    item_group.appendChild(item).appendChild(text).appendChild(cat_text_tag);
                }


                let traffic_text = dataobj.data[i]["mrt"];
                if (traffic_text != null) {
                    traffic_text.className = "traffic";
                    let traffic_text_tag = document.createElement("div");
                    traffic_text_tag.className = "traffic";
                    traffic_text_tag.textContent = traffic_text;
                    item_group.appendChild(item).appendChild(text).appendChild(traffic_text_tag);
                }

            }
            let pagenum = dataobj.nextPage;
            return pagenum;
        })
        .then(scroll => {
            nextpage = scroll;
            console.log("下一頁:" + nextpage);

            // scroll事件
            window.onscroll = function () {
                const footer = document.querySelector("footer")
                // console.log("scroll: " + this.scrollY + " innerHeight: " + this.innerHeight + "頁尾: " + footer.offsetTop);
                if (this.scrollY + this.innerHeight > footer.offsetTop) {
                    // scroll事件
                    var timeout;
                    window.onscroll = function () {
                        clearTimeout(timeout);
                        timeout = setTimeout(function () {
                            if (nextpage == null) {
                                console.log("stop");
                            } else {
                                console.log("頁碼: " + nextpage);
                                const url = `/api/attractions?page=${nextpage}`;
                                queryImg(nextpage, url);
                            }

                        }, 100);
                    }
                }
            };
        })
    // 結束畫面
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "none"
    };

}



//關鍵字搜尋==================================================
//開啟連線
let button = document.getElementById("buttonId");
function clickButton(e) {
    e.preventDefault();
    keyword = document.getElementById("keyword").value;
    // 刪除attractions-group舊圖片
    let parent = document.getElementById("attractions");
    let child = document.getElementById("attractions-group");
    parent.removeChild(child);
    //產生attractions-group新圖片
    let item_group = document.createElement("div");
    item_group.className = "attractions-group";
    item_group.id = "attractions-group";
    parent.appendChild(item_group);

    const url = `/api/attractions?page=${page}&keyword=${keyword}`;

    if (page != null) {
        queryAttraction(page, keyword, url);
    } else {
        console.log("無資料");
    }


    //執行函式

    function queryAttraction(page, keyword, url) {
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
                console.log(dataobj.data)

                //查無資料
                if (dataobj.data.length === 0) {
                    console.log("nodata")
                    document.getElementById("attractions-group").innerHTML = "查無資料"


                } else {
                    for (let i = 0; i < dataobj.data.length; i++) {
                        // 框架

                        let item = document.createElement("div");
                        item.className = "attraction-desktop";
                        item.id = "attraction-desktop";
                        //取得景點編號
                        function clickId(e) {
                            e.preventDefault();
                            id = this.getAttribute('id');
                            let url_id = "/attraction/" + id;
                            window.location.href = url_id;
                        }

                        //景點編號
                        item.id = dataobj.data[i]["id"];
                        item.addEventListener("click", clickId);

                        //圖片
                        let url_img = dataobj.data[i]["images"][0];
                        let image = new Image();
                        image.src = url_img
                        image.className = "img";

                        item_group.appendChild(item).appendChild(image);


                        //文字
                        let text = document.createElement("div");
                        text.className = "text_attraction";
                        text.id = "text";

                        let title_text = dataobj.data[i]["name"];
                        if (title_text != null) {
                            title_text.className = "title";
                            let title_text_tag = document.createElement("div");
                            title_text_tag.className = "title";
                            title_text_tag.textContent = title_text;
                            item_group.appendChild(item).appendChild(title_text_tag);

                        }

                        let cat_text = dataobj.data[i]["category"];
                        if (cat_text != null) {
                            cat_text.className = "cat";
                            let cat_text_tag = document.createElement("div");
                            cat_text_tag.className = "cat";
                            cat_text_tag.textContent = cat_text;
                            item_group.appendChild(item).appendChild(text).appendChild(cat_text_tag);
                        }


                        let traffic_text = dataobj.data[i]["mrt"];
                        if (traffic_text != null) {
                            traffic_text.className = "traffic";
                            let traffic_text_tag = document.createElement("div");
                            traffic_text_tag.className = "traffic";
                            traffic_text_tag.textContent = traffic_text;
                            item_group.appendChild(item).appendChild(text).appendChild(traffic_text_tag);
                        }



                    }
                    const pagenum = dataobj.nextPage;
                    return pagenum;
                }
            })
            .then(scroll => {
                nextpage = scroll;
                // scroll事件
                window.onscroll = function () {
                    const footer = document.querySelector("footer")
                    // console.log("scroll: " + this.scrollY + " innerHeight: " + this.innerHeight + "頁尾: " + footer.offsetTop);
                    if (this.scrollY + this.innerHeight > footer.offsetTop) {
                        // scroll事件
                        var timeout;
                        window.onscroll = function () {
                            clearTimeout(timeout);
                            timeout = setTimeout(function () {
                                if (nextpage == null) {
                                    // console.log("stop");
                                } else {
                                    console.log("頁碼: " + nextpage);
                                    const url = `/api/attractions?page=${nextpage}&keyword=${keyword}`;
                                    queryAttraction(page, keyword, url);
                                }

                            }, 100);
                        }
                    }
                };
            })
            .catch(err => {
                console.log(err.response.data);
            });
    }

}
button.addEventListener("click", clickButton);


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

    }



}

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

    function signinReq() {
        fetch('/api/user', options)
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

    }

<<<<<<< HEAD
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

        async function signupReq() {
            await fetch('/api/user', options)
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
=======
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a


}

// 關閉登入視窗(外層)=================================================    
let outerPagelogin = document.getElementById("login-bgPage");
outerPagelogin.addEventListener("click", loginClose);
function loginClose() {
    document.getElementById("loginPage").style.display = "none";
    console.log("關閉視窗")

<<<<<<< HEAD
    }

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
}
let outerPagesignup = document.getElementById("signup-bgPage");
outerPagesignup.addEventListener("click", signupClose);
function signupClose() {
    document.getElementById("signupPage").style.display = "none";
    document.getElementById("loginPage").style.display = "none";

}
>>>>>>> 4c02531a3bf90206e3bb2556f05648a7f01faa7a

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

//預定行程=========================================
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


}


