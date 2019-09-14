//自定義方法

//發送ajax post請求 data:傳送的資料 url:請求的url handleResponse: success後的callback function
//須先在html頁面的script 設置window.CSRF_TOKEN = "{{ csrf_token }}"
function PostAjaxJsonRequest(data, url, handleResponse) {
    $.ajax({
        headers: { "X-CSRFToken": window.CSRF_TOKEN },
        url: url,
        type: "post",
        data: data,
        dataType: "json",
        success: function (response) {
            handleResponse(response);
        },
        error: function () {
            kendo.alert("系統異常");
        }
    })
}
