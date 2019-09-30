// 主要處理登入權限等事情

$(function() {
    const $btnLogin = $('loginSubmitBtn');
    const $username = $('uname');
    const $password = $('psw');

    // 登入視窗初始化
    $("#loginWindow").kendoWindow({
        width:"600px",
        title: "登入",
        visible: false,
        modal: true,
        actions: [
            "Maximize",
            "Close"
        ]
    }).data("kendoWindow").center();

    $btnLogin.click(function(e){
        const username = $username.val();
        const password = $password.val();

    });

///////////////////////// Tab Setting ///////////////////////////////////////////
    $('#login-form-link').click(function(e) {
    		$("#login-form").delay(100).fadeIn(100);
     		$("#register-form").fadeOut(100);
    		$('#register-form-link').removeClass('active');
        $("#forgotPassword-form").fadeOut(100);
        $('#forgotPassword-form-link').removeClass('active');
    		$(this).addClass('active');
    		e.preventDefault();
  	});

  	$('#register-form-link').click(function(e) {
  		$("#register-form").delay(100).fadeIn(100);
   		$("#login-form").fadeOut(100);
  		$('#login-form-link').removeClass('active');
      $("#forgotPassword-form").fadeOut(100);
      $('#forgotPassword-form-link').removeClass('active');
  		$(this).addClass('active');
  		e.preventDefault();
  	});

    $('#forgotPassword-form-link').click(function(e) {
  		$("#forgotPassword-form").delay(100).fadeIn(100);
   		$("#login-form").fadeOut(100);
  		$('#login-form-link').removeClass('active');
      $("#register-form").fadeOut(100);
      $('#register-form-link').removeClass('active');
  		$(this).addClass('active');
  		e.preventDefault();
  	});
/////////////////////////////////////////////////////////////////////////

  //註冊請求
    $("#registerForm").submit(function(e){
      e.preventDefault();
      PostAjaxJsonRequest($("#registerForm").serialize(), "/accounts/register/", function(response){
        if(response.success){
          alert(response.messages);
          location.reload(); //重整頁面
        }else{
          alertMessage(response.messages);
        }
      });
      return false;
    });

    //發送忘記密碼請求
    $("#forgotPasswordForm").submit(function(e){
      e.preventDefault();
      PostAjaxJsonRequest($("#forgotPasswordForm").serialize(), "/accounts/SendVerificationCode/", function(response){
        if(response.success){
          alert(response.messages);
          location.reload(); //重整頁面
        }else{
          alertMessage(response.messages);
        }
      });
      return false;
    });

    //登入請求
    $("#loginForm").submit(function(e){
      e.preventDefault();
      PostAjaxJsonRequest($("#loginForm").serialize(), "/accounts/login/", function(response){
        if(response.success){
          location.reload(); //重整頁面
        }else{
          alert(response.messages);
        }
      });
      return false;
    });

    //登出請求
    $("#Btnlogout").click(function(){
      PostAjaxJsonRequest(null, "/accounts/logout/", function(response){
        if(response.success){
          location.reload(); //重整頁面
        }
      });
    })
});

$("#btn-login").click(function() {
  $("#loginWindow").data("kendoWindow").open().center();
  console.log($( window ).width());
  console.log($( window ).width() <= 600);
  if($( window ).width() <= 600){
    $("#loginWindow").data("kendoWindow").maximize();
  }else{
    $("#loginWindow").data("kendoWindow").restore();
  }
})
