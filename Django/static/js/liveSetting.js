function onOpenLiveButtonClick() {
    $("#streamForm").submit();
}

function onCloseLiveButtonClick() {
    $('#youtubeUrl').val('');
    $('#introduction').val('');
    $('#state').val('0');
    $("#streamForm").submit();
}
