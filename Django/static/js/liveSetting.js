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
      $("#streamForm").submit();
    /*else {
        $.ajax({
            url: 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + $('#youtubeUrl').val() + '&key=' + youtubeApiKey,
            async: false,
            dataType: 'json',
            success: function(data) {
                if (data['items'].length != 0) {
                    console.log("Successfully connected youtube.");
                    $("#streamForm").submit();
                }
                else {
                    $('#message').text("The Youtube vid does not exist.");
                }
            },
            error: function() {
                console.log("Failed to connect youtube.");
            }
        });
    }*/
}

function onCloseLiveButtonClick() {
    $('#youtubeUrl').val('');
    $('#category').val('');
    $('#introduction').val('');
    $('#state').val('0');
    $("#streamForm").submit();
}
