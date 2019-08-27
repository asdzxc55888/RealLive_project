document.querySelector('#openDetection').addEventListener('click', onOpenDetectionButtonClick);
document.querySelector('#closeDetection').addEventListener('click', onCloseDetectionButtonClick);
player = document.getElementById('player')
canvas = document.getElementById('snapshot')
context = canvas.getContext('2d');

var track;

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
    var data = canvas.toDataURL('image/jpeg', 1.0);
    var blob = new Blob([data.buffer]);
}
