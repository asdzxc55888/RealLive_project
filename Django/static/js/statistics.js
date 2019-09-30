// This code loads the IFrame Player API code asynchronously
var tag = document.createElement('script');
tag.src = "http://www.youtube.com/iframe_api";

// Inserting this script
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

function onPlayerReady(event) {
    event.target.playVideo();
}

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

function uploadVideo(vid) {
	var thumbSize = 'large',
		imgWidth = '200',
		imgHeight = '150',
		address = 'https://www.youtube.com/watch?v=' + vid;
	var _type = (thumbSize == 'large') ? 0 : 2;

	try {
		// 取得 title
		var title = 'None';
		$.ajax({
			url: 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + vid + '&key=' + youtubeApiKey,
			async: false,
			dataType: 'json',
			success: function(data) {
				console.log("Successfully obtained information.");
				title = (data['items'][0]['snippet']['title']);
			},
			error: function() {
				console.log("Failed to get the data, see network tab for response details.");
			}
		});

		// 取得縮圖
		var thumbUrl = "http://img.youtube.com/vi/" + vid + "/" + _type + ".jpg";

		var html = '<li class="row"><a class="col-md-6" href="' + address + '">';
		html += '<img src="' + thumbUrl + '" alt="' + title + '" title="' + title + '" width="' + imgWidth + '" height="' + imgHeight + '" />';
		html += '</a><p class="col-md-6 videoTitle">' + title + '</p></li>';

		var option = htmlToElement(html);
		$(option).children('a').click(function() {
			var form = document.getElementById("vidForm");
			var input = document.getElementById("vidInput");
		    input.setAttribute("value", vid);
		    form.submit();
			return false;
		});

		$('.playlist').append(option);
	}
	catch {
		alert('很抱歉無法連接vid=' + vid + '的直播紀錄');
	};
}

function loadChatRecord(vid){
  var data = { "vid":vid };
  var url = "/statistics/getChatRecord"
  console.log(vid);
  PostAjaxJsonRequest(data, url, function(response){
    var chatMessage = "";
    for (var message in response) {
      chatMessage += response[message] + "\n";
    }
    console.log(chatMessage)
    $("#chat-log").val(chatMessage);
  });
}

function updateSelecter(hours) {
	if (hours > 1) {
		var content = '<select id="section" style="margin: 0 auto" onchange="changeSection()">';
		for (i = 1; i <= hours; i++) {
			content += '<option value="' + String(i) + '">' + String(i - 1) + ' ~ ' + String(i) + ' hours</option>';
		}
		content += '</select>';
		document.getElementById('selecter').innerHTML = content;
	}
}

function changeSection() {
    var s = $('#section').children("option:selected").val();
    myChart.destroy();
    createChart(t.slice((s - 1) * 3600, s * 3600), angey.slice((s - 1) * 3600, s * 3600), disgust.slice((s - 1) * 3600, s * 3600),
                fear.slice((s - 1) * 3600, s * 3600), happy.slice((s - 1) * 3600, s * 3600), sad.slice((s - 1) * 3600, s * 3600),
                surprise.slice((s - 1) * 3600, s * 3600));
}

function setChartWidth(n) {
	var w = $('.chartWrapper').width();
	if (n * 10 > w && n * 10 < 16000)
		w = n * 10;
	else if (n * 10 > w) {
		w = 16000;
	}
	$('.chartAreaWrapper').css("width", w);
}

function toSecond(time) {
    var t = time.split(':');
    return Number(t[0]) * 3600 + Number(t[1]) * 60 + Number(t[2]);
}

function createChart(time, angryData, disgustData, fearData, happyData, sadData, surpriseData) {
	var ctx = document.getElementById('myChart');
	myChart = new Chart(ctx, {
		type: 'line',
		data: {
			labels: time,
			datasets: [{
				label: 'Angry',
				data: angryData,
				backgroundColor: 'rgba(255, 99, 132, 0.5)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 3,
				fill: false,
				hidden: true
			}, {
				label: 'Happy',
				data: happyData,
				backgroundColor: 'rgba(255, 159, 64, 0.7)',
				borderColor: 'rgba(255, 159, 64, 1)',
				borderWidth: 3,
				fill: false
			}, {
				label: 'Surprise',
				data: surpriseData,
				backgroundColor: 'rgba(255, 205, 86, 0.5)',
				borderColor: 'rgba(255, 205, 86, 1)',
				borderWidth: 3,
				fill: false,
				hidden: true
			}, {
				label: 'Disgust',
				data: disgustData,
				backgroundColor: 'rgba(75, 192, 192, 0.5)',
				borderColor: 'rgba(75, 192, 192, 1)',
				borderWidth: 3,
				fill: false,
				hidden: true
			}, {
				label: 'Sad',
				data: sadData,
				backgroundColor: 'rgba(54, 162, 235, 0.5)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 3,
				fill: false,
				hidden: true
			}, {
				label: 'Fear',
				data: fearData,
				backgroundColor: 'rgba(153, 102, 255, 0.5)',
				borderColor: 'rgba(153, 102, 255, 1)',
				borderWidth: 3,
				fill: false,
				hidden: true
			}]
		},
		options: {
			responsive: true,
            maintainAspectRatio: false,
			scales: {
				xAxes: [{
					ticks: {
						maxTicksLimit: 60
					}
				}],
				yAxes: [{
					ticks: {
						beginAtZero: false
					}
				}]
			},
			legend: {
				display: true,
				position: 'left',
				labels: {
					padding: 60
				}
			},
			elements: {
                point: {
                    radius: 0,
					hitRadius: 5
                }
            }
		},
	});

    // seek youtube video to click point
    ctx.onclick = function(evt) {
        var activePoint = myChart.getElementsAtEvent(evt)[0];

        if (activePoint !== undefined) {
            var time = myChart.data.labels[activePoint._index];
            player.seekTo(toSecond(time));
        }
    };
}
