function getData() {
    //取得關鍵字
    let keyword = document.getElementById("keyword").value;
    //預設頁碼
    let page = 0;

    // 定義url
    if (keyword != "") {
        const url = `http://127.0.0.1:3000/api/attractions?page=${page}&keyword=${keyword}`;
        if (page != null) {
            queryAttraction(page, keyword, url);
        } else {
            console.log("無資料");
        }

    } else {
        const url = `http://127.0.0.1:3000/api/attractions?page=${page}`;
        if (page != null) {
            queryImg(page, url);
        } else {
            console.log("無資料");
        }
    }

    // 有圖片、無關鍵字

    async function queryImg(page, url) {
        await fetch(url)
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
                    item.id = "attraction-desktop";

                    //圖片

                    let url_img = dataobj.data[i]["images"][0];
                    let image = new Image();
                    image.src = url_img
                    image.className = "img";
                    let image_tag = document.createElement("div");
                    item_group.appendChild(item).appendChild(image_tag).appendChild(image);

                    //文字
                    let cat_text = dataobj.data[i]["category"];
                    if (cat_text != null) {
                        cat_text.className = "cat";
                        let cat_text_tag = document.createElement("div");
                        cat_text_tag.className = "cat";
                        cat_text_tag.textContent = cat_text;
                        item_group.appendChild(item).appendChild(cat_text_tag);
                    }


                    let traffic_text = dataobj.data[i]["mrt"];
                    if (traffic_text != null) {
                        traffic_text.className = "traffic";
                        let traffic_text_tag = document.createElement("div");
                        traffic_text_tag.className = "traffic";
                        traffic_text_tag.textContent = traffic_text;
                        item_group.appendChild(item).appendChild(traffic_text_tag);
                    }


                    let title_text = dataobj.data[i]["name"];
                    if (title_text != null) {
                        title_text.className = "title";
                        let title_text_tag = document.createElement("div");
                        title_text_tag.className = "title";
                        title_text_tag.textContent = title_text;
                        item_group.appendChild(item).appendChild(title_text_tag);

                    }
                }
                const pagenum = dataobj.nextPage;
                // console.log("下一頁:" + pagenum);
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
                                    const url = `http://127.0.0.1:3000/api/attractions?page=${nextpage}`;
                                    queryImg(nextpage, url);
                                }

                            }, 100);
                        }
                    }
                };
            })
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



        const url = `http://127.0.0.1:3000/api/attractions?page=${page}&keyword=${keyword}`;

        if (page != null) {
            queryAttraction(page, keyword, url);
        } else {
            console.log("無資料");
        }


        //執行函式

        async function queryAttraction(page, keyword, url) {
            await fetch(url)
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
                            //圖片
                            let url_img = dataobj.data[i]["images"][0];
                            let image = new Image();
                            image.src = url_img
                            image.className = "img";
                            let image_tag = document.createElement("div");

                            item_group.appendChild(item).appendChild(image_tag).appendChild(image);


                            //文字
                            let cat_text = dataobj.data[i]["category"];
                            if (cat_text != null) {
                                cat_text.className = "cat";
                                let cat_text_tag = document.createElement("div");
                                cat_text_tag.className = "cat";
                                cat_text_tag.textContent = cat_text;
                                item_group.appendChild(item).appendChild(cat_text_tag);
                            }


                            let traffic_text = dataobj.data[i]["mrt"];
                            if (traffic_text != null) {
                                traffic_text.className = "traffic";
                                let traffic_text_tag = document.createElement("div");
                                traffic_text_tag.className = "traffic";
                                traffic_text_tag.textContent = traffic_text;
                                item_group.appendChild(item).appendChild(traffic_text_tag);
                            }


                            let title_text = dataobj.data[i]["name"];
                            if (title_text != null) {
                                title_text.className = "title";
                                let title_text_tag = document.createElement("div");
                                title_text_tag.className = "title";
                                title_text_tag.textContent = title_text;
                                item_group.appendChild(item).appendChild(title_text_tag);

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
                                        const url = `http://127.0.0.1:3000/api/attractions?page=${nextpage}&keyword=${keyword}`;
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

}


