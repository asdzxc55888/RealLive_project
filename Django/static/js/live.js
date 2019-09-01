var player = document.getElementById('player')
var canvas = document.getElementById('snapshot')
var context = canvas.getContext('2d');
var track;

// connect image socket
var imageSocket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname + 'image');

imageSocket.onopen = function(e) {
    console.log('Image socket connected.');
};

imageSocket.onclose = function(e) {
    console.error('Image socket closed unexpectedly.');
};

function onOpenDetectionButtonClick() {
    // labeload user's picture
    navigator.mediaDevices.getUserMedia({video: true})
    .then(mediaStream => {
        document.querySelector('video').srcObject = mediaStream;
        track = mediaStream.getVideoTracks()[0];
        // run storePicture every seconds
        timer = setInterval(storePicture, 1000);
    })
    .catch(function(err) { console.log(err.name + ": " + err.message); });
}

function onCloseDetectionButtonClick() {
    track.stop();
    // stop running storePicture
    clearInterval(timer);
}

function storePicture() {
    context.drawImage(player, 0, 0, 320, 240);
    canvas.toBlob(function(blob){
        imageSocket.send(blob);
    }, "image/jpeg", 1.0);
}
