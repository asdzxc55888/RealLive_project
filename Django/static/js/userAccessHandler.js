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

    $('#login-form-link').click(function(e) {
    		$("#login-form").delay(100).fadeIn(100);
     		$("#register-form").fadeOut(100);
    		$('#register-form-link').removeClass('active');
    		$(this).addClass('active');
    		e.preventDefault();
  	});
    
  	$('#register-form-link').click(function(e) {
  		$("#register-form").delay(100).fadeIn(100);
   		$("#login-form").fadeOut(100);
  		$('#login-form-link').removeClass('active');
  		$(this).addClass('active');
  		e.preventDefault();
  	});

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
