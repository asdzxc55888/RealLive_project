// This code loads the IFrame Player API code asynchronously
var tag = document.createElement('script');
tag.src = "http://www.youtube.com/iframe_api";

// Inserting this script
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


function onPlayerReady(event) {
    event.target.playVideo();
}

function onOpenLiveButtonClick() {
    reg = /[a-zA-Z0-9\-_]/;
    if (!reg.test($('#youtubeUrl').val()) || $('#youtubeUrl').val().length != 11)
    {
        $('#message').text('Youtube vid error.');
    }
    else
        $('#streamForm').submit();
}

function onCloseLiveButtonClick() {
    $('#youtubeUrl').val('');
    $('#category').val('聊天');
    $('#introduction').val('');
    $('#state').val('0');
    $('#streamForm').submit();
}
