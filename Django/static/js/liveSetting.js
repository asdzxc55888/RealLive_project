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
    if ($("#category").val() == "") {
        $('#message').text("Live category cannot be blank.");
    }
    else {
        $("#streamForm").submit();
    }
}

function onCloseLiveButtonClick() {
    $('#youtubeUrl').val('');
    $('#category').val('');
    $('#introduction').val('');
    $('#state').val('0');
    $("#streamForm").submit();
}
