// Get the 註冊modal
var signUpModal = document.getElementById('signUpForm');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == signUpModal) {
        signUpModal.style.display = "none";
    }
}

// event setup
$(document).ready(function() {
    const $btnLogin = $('BtnloginSubmit');
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

    $btnLogin.click(function(e){
        const username = $username.val();
        const password = $password.val();
        
    });

    $("#btn-login").click(function() {
        $("#loginForm").data("kendoWindow").open();
    })
});
function clickLoginBtn() {
    $("#btn-login").click(function() {
        $("#loginForm").data("kendoWindow").open();
    })
}