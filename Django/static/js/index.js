$(document).ready(function () {
    loadBookData();
    $("#streamer_grid").kendoGrid({
        dataSource: { 
            transport: {
                read: {
                    type:"post",
                    url: "/getStreamer",
                    dataType: "json"
                }
            },
            schema: {
                model: {
                    fields: {
                        StreamerName: { type: "string" },
                        Introduction: { type: "string" },
                        ViewerNumber: { type: "int" },
                        StreamerUserName: { type: "string" }
                    }
                }
            },
            pageSize: 20,
        },
        toolbar: kendo.template("<div class='streamer-grid-toolbar'><input class='streamer-grid-search' placeholder='尋找實況主......' type='text'></input></div>"),
        height: 550,
        sortable: true,
        pageable: {
            input: true,
            numeric: false
        },
        columns: [
            { field: "StreamerName", title: "實況主名稱", width: "10%" },
            { field: "Introduction", title: "簡介", width: "70%" },
            { field: "ViewerNumber", title: "觀看次數", width: "10%" },
            { field: "StreamerUserName", width: "0%" },
            { command: { text: "前往頻道", click: gotoChannel }, title: " ", width: "180px" }
        ]
    });
});

function loadBookData() {
    testDataLocalStorage = JSON.parse(localStorage.getItem("testData"));
    if (testDataLocalStorage == null) {
        testDataLocalStorage = testData;
        localStorage.setItem("testData", JSON.stringify(testDataLocalStorage));
    }
}

function gotoChannel(e) {
    var grid = $("#streamer_grid").data("kendoGrid");
    var dataItem = grid.dataItem($(e.currentTarget).closest("tr"));
    window.location.href = "/live/" + dataItem.StreamerUserName;
}

