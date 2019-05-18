// Get the 登入modal
var loginModal = document.getElementById('loginForm');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == loginModal) {
        loginModal.style.display = "none";
    }
}

// Get the 註冊modal
var signUpModal = document.getElementById('signUpForm');

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    if (event.target == signUpModal) {
        signUpModal.style.display = "none";
    }
}

$(document).ready(function () {
    const $btnLogin = $('BtnloginSubmit');
    const $username = $('uname');
    const $password = $('psw');

    $btnLogin.click(function(e){
        const username = $username.val();
        const password = $password.val();
        
    });
});