// event setup
$(function() {
    const $btnLogin = $('loginSubmitBtn');
    const $username = $('uname');
    const $password = $('psw');

    $("#loginForm").kendoWindow({
        width: "600px",
        title: "登入",
        visible: false,
        modal: true,
        actions: [
            "Close"
        ]
    }).data("kendoWindow").center();

    // $("#registerForm").kendoWindow({
    //     width: "600px",
    //     height : "600px",
    //     title: "註冊",
    //     visible: false,
    //     modal: true,
    //     actions: [
    //         "Close"
    //     ]
    // }).data("kendoWindow").center();

    $btnLogin.click(function(e){
        const username = $username.val();
        const password = $password.val();

    });

    $("#btn-login").click(function() {
        $("#loginForm").data("kendoWindow").open();
    })

  /*  $("#registerForm").submit(function(e) {
      e.preventDefault();
      csrfmiddlewaretoken = $("registerForm").find("input[name='csrfmiddlewaretoken']" ).val();
        $.ajax({
               type: "POST",
               url: "/accounts/register/",

               data: {
                 "form" : $("#registerForm").serialize(),
                 "csrfmiddlewaretoken" : csrfmiddlewaretoken
               },
               success: function(data)
               {
                   alert("註冊成功");
               },
               error:function()
               {
                  alert("註冊失敗！請確認資料是否符合要求");
               }
             });

        return false;
    });*/
});

function clickLoginBtn() {
    $("#btn-login").click(function() {
        $("#loginForm").data("kendoWindow").open();
    })
}

// function ShowRegisterForm() {
//   $("#loginForm").data("kendoWindow").close();
//   $("#registerForm").data("kendoWindow").open();
// }
