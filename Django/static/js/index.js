$(document).ready(function () {

    $("#streamer_grid").jsGrid({
        height: "auto",
        width: "100%",

        sorting: true,
        paging: true,
        autoload: true,
        controller: {
            loadData: function(){
                return $.ajax({
                    url: '/getStreamer',
                    type: 'post',
                    dataType: 'json'
                });
            }
        },

        fields: [
            { name: "StreamerUserName", css:"hide" }, // hide:custom pemater from style.css
            { name: "StreamerName", title: "實況主名稱", type: "text", width: "15%" },
            {
                itemTemplate: function(_, item) {
                    return $(getYoutubeImage(item.vid))
              	},width: "15%"
            },
            { name: "Category", title: "實況類別", type: "text", width: "10%" },
            { name: "Introduction", title: "簡介", type: "text", width: "45%" },
            {
                itemTemplate: function(_, item) {
                    return $('<button class="goToBtn">').text("前往頻道")
                    	.on("click", function() {
                            window.location.href="/live/" + item.StreamerUserName;   //導向直播頁面
                    	});
              	}
            }
        ]
    });
});

//取得yt縮圖 return： html img tag
function getYoutubeImage(vid){
  var imgWidth = '250',
      imgHeight = '175';
  var title = 'None';
  $.ajax({
    url: 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + vid + '&key=' + youtubeApiKey,
    async: false,
    dataType: 'json',
    success: function(data) {
      //console.log("Successfully obtained information.");
      title = (data['items'][0]['snippet']['title']);
    },
    error: function() {
      //console.log("Failed to get the data, see network tab for response details.");
    }
  });

  // 取得縮圖
  var thumbUrl = "http://img.youtube.com/vi/" + vid + "/0.jpg";

  var result = '<img src="' + thumbUrl + '" alt="' + title + '" title="' + title + '" width="' + imgWidth + '" height="' + imgHeight + '" />';
  return result;
}

var loadData = function (e) {
    console.log("loadData");
    //==============定義延遲載入
    var d = $.Deferred();
    //=================服務端分頁需要將頁面索引傳遞到服務端=======================
    pageSize = e.pageSize;
    pageIndex = e.pageIndex;
    $.ajax({
        url: '/getStreamer',
        type: 'post',
        dataType: 'json'
    }
    ).done(function (response) {
        //===========================服務端分頁的話就沒必要取子集了=========================
        subdata = response.slice(pageSize * (pageIndex - 1), pageSize * pageIndex);
        pagingdata = { data: response, itemsCount: response.length };
        //console.log(response);
        //console.log(subdata);
        //console.log(pagingdata);
        //============服務端完成時發出完成通知==================
        d.resolve(pagingdata);
    }).fail(function (e) {
        alert('load data failed!');
    });
    //=============向loadData返回延遲載入方法===================
    return d.promise();
};
