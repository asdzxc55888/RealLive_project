var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws' + window.location.pathname);

chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#chat-log').value += (message + '\n');
    var textarea = document.getElementById('chat-log');
    textarea.scrollTop = textarea.scrollHeight;
    //console.log('message:' + message)
};

chatSocket.onopen = function (e) {
    console.log('Chat socket connected.');
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly.');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    if(messageInputDom.value != ''){
      var username = $("#username").html();
      if(username !== undefined){
        var message = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'username' : username,
            'message': message,
            'vid': vid
        }));
      }else{
        alert("請先登入後才能進行發言！");
      }
      messageInputDom.value = '';
    }
};
