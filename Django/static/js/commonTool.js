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

//跳出alert視窗 messages為Array of Object
function alertMessage(messages){
  var messageArray = Object.values(messages);
  var resultMessage = "";
  for (var i = 0; i < messageArray.length; i++) {
    resultMessage += messageArray[i] + "\r\n";
  }
  alert(resultMessage);
}
