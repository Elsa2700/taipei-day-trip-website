
//載入頁面，檢查使用者狀態=========================================
querybookingState();
function querybookingState() {
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "block"
    };
    fetch("/api/user")
        .then(res => {
            return res.json();
        })
        .then(result => {
            let dataobj = result;

            if (dataobj["data"] == null) {
                //判斷式:null(未登入):導向首頁
                window.location.href = "/";

            } else {
                //判斷式:不為null(已登入)
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

                    function signoutReq() {
                        fetch('/api/user', options)
                            .then(res => {
                                return res.json();
                            })
                            .then(result => {
                                let dataobj = result;
                                if (dataobj["ok"] == true) {
                                    //重新載入頁面
                                    window.document.location.reload();
                                }
                            })

                    };


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
        window.onload = function () {
            let load = document.getElementById("load");
            load.style.display = "block"
        };
        fetch("/api/user")
            .then(res => {
                return res.json();
            })
            .then(result => {
                let dataobj = result;

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


let url = location.href;
let orderNum = url.split('number=')[1]
console.log(orderNum);
//歡迎會員標頭說明
let orderNum_text = document.getElementById("orderNum_thank");
orderNum_text.textContent = orderNum;

//顯示訂單成立的畫面
let url_thank = "/api/order/" + orderNum
queryThankyou(url_thank);
function queryThankyou(url_thank) {
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "block"
    };
    fetch(url_thank)
        .then(res => {
            return res.json();
        })
        .then(result => {
            let img2 = result["data"]["trip"]["attraction"]["image"][1]
            let thankyou_icon = document.getElementById("thankyou_icon");
            thankyou_icon.classList = "icon1";
            thankyou_icon.style.backgroundImage = "url(" + img2 + ")";
            let ordername = result["data"]["contact"]["name"];
            let ordername_icon = document.getElementById("order_name");
            ordername_icon.textContent = ordername;
            let emailmsg = document.getElementById("msg");
            emailmsg.textContent = result["message"];
        })
    // 結束畫面
    window.onload = function () {
        let load = document.getElementById("load");
        load.style.display = "none"
    };
}





