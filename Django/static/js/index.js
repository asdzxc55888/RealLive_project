testData = [{
    "StreamerName":"老大",
    "Introduction":"老大屁股大",
    "ViewerNumber":"100"
},{
    "StreamerName":"Bang大便",
    "Introduction":"Bang拉",
    "ViewerNumber":"1000"
}]

var testDataLocalStorage = [];

$(document).ready(function() {
    loadBookData();
    $("#streamer_grid").kendoGrid({
        dataSource: {
            data: testData,
            schema: {
                model: {
                    fields: {
                        StreamerName: { type: "string" },
                        Introduction: { type: "string" },
                        ViewerNumber: { type: "int" }
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
            { command: { text: "前往頻道", click: toChannel }, title: " ", width: "180px" }
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

function toChannel() {

}

