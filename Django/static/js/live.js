var stream = document.getElementById('stream'),
    snapshot = document.getElementById('snapshot'),
    snapshotContext = snapshot.getContext('2d'),
    test = document.getElementById('test'),
    track, timer, videoWidth, videoHeight;

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
    $('#openDetection').prop('disabled', true);
    $('#closeDetection').prop('disabled', false);
    // labeload user's picture
    navigator.mediaDevices.getUserMedia({video: true})
    .then(mediaStream => {
        document.querySelector('video').srcObject = mediaStream;
        stream.onloadeddata = function() {
            videoWidth = stream.videoWidth / 2;
            videoHeight = stream.videoHeight / 2
            $('#snapshot').prop('width', videoWidth);
            $('#snapshot').prop('height', videoHeight);
        };
        track = mediaStream.getVideoTracks()[0];
        // run storePicture every seconds
        timer = setInterval(storePicture, 1000);
    })
    .catch(function(err) { console.log(err.name + ": " + err.message); });
}

function onCloseDetectionButtonClick() {
    $('#openDetection').prop('disabled', false);
    $('#closeDetection').prop('disabled', true);
    stopGettingPicture();
}

function storePicture() {
    if (isPlay)
    {
        snapshotContext.drawImage(stream, 0, 0, videoWidth, videoHeight);
        snapshot.toBlob(function(image){
            var time = Math.floor(player.getCurrentTime()).toString();
            imageSocket.send(new Blob([vid + ' ' + time], {type : 'text/plain'}));
            imageSocket.send(image);
        }, "image/jpeg", 1.0);
    }
}

function stopGettingPicture() {
    track.stop();
    // stop running storePicture
    clearInterval(timer);
    timer = null;
}
