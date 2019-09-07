var player = document.getElementById('player');
var snapshot = document.getElementById('snapshot');
var snapshotContext = snapshot.getContext('2d');
var test = document.getElementById('test');
var track;

// connect image socket
var imageSocket = new WebSocket('ws://' + window.location.host + '/ws' + window.location.pathname + 'image');

imageSocket.onopen = function(e) {
    console.log('Image socket connected.');
};

imageSocket.onclose = function(e) {
    console.error('Image socket closed unexpectedly.');
};

imageSocket.onmessage = function(e) {
    var reader = new FileReader();
    reader.readAsDataURL(e.data);
    reader.onloadend = function() {
        var base64data = reader.result;
        test.src = 'data:image/jpg;base64,' + base64data.split(",")[1];
    }
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
    snapshotContext.drawImage(player, 0, 0, 320, 240);
    snapshot.toBlob(function(blob){
        imageSocket.send(blob);
    }, "image/jpeg", 1.0);
}
