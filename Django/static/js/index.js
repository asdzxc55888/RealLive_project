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
            { name: "StreamerName", title: "實況主名稱", type: "text", width: "10%" },
            { name: "Introduction", title: "簡介", type: "text", width: "70%" },
            { name: "ViewerNumber", title: "觀看次數", type: "text", width: "10%" },
            { name: "StreamerUserName", width: 0, visible: false },
            {
                itemTemplate: function(_, item) {
                    return $("<button>").text("前往頻道")
                    	.on("click", function() {
                            window.location.href="/live/" + item.StreamerUserName;   //導向直播頁面
                    	});
              	}
            }
        ]
    });
});

function gotoChannel(e) {
    var grid = $("#streamer_grid").data("kendoGrid");
    var dataItem = grid.dataItem($(e.currentTarget).closest("tr"));
    window.location.href = "/live/" + dataItem.StreamerUserName;
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
        console.log(response);
        console.log(subdata);
        console.log(pagingdata);
        //============服務端完成時發出完成通知==================
        d.resolve(pagingdata);
    }).fail(function (e) {
        alert('load data failed!');
    });
    //=============向loadData返回延遲載入方法===================
    return d.promise();
};
