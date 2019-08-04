var chatSocket = new WebSocket(
    'ws://' + window.location.host +
    '/ws' + window.location.pathname + '/');

chatSocket.onmessage = function (e) {
    var data = JSON.parse(e.data);
    var message = data['message'];
    document.querySelector('#chat-log').value += (message + '\n');
    console.log('message:' + message)
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
    console.log('close:')
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    var messageInputDom = document.querySelector('#chat-message-input');
    var message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message
    }));
    console.log('send:')

    messageInputDom.value = '';
};