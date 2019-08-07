function playVideo(vid) {
	$('#player').attr('src', 'https://www.youtube.com/embed/' + vid);
}

function createChart(time, angryData, disgustData, fearData, happyData, sadData, surpriseData, neutralData) {
	var ctx = document.getElementById('myChart');
	var myChart = new Chart(ctx, {
		type: 'bar',
		data: {
			labels: time,
			datasets: [{
				label: 'Angry',
				data: angryData,
				backgroundColor: 'rgba(255, 99, 132, 0.5)',
				borderColor: 'rgba(255, 99, 132, 1)',
				borderWidth: 1
			}, {
				label: 'Disgust',
				data: disgustData,
				backgroundColor: 'rgba(75, 192, 192, 0.5)',
				borderColor: 'rgba(75, 192, 192, 1)',
				borderWidth: 1
			}, {
				label: 'Fear',
				data: fearData,
				backgroundColor: 'rgba(153, 102, 255, 0.5)',
				borderColor: 'rgba(153, 102, 255, 1)',
				borderWidth: 1
			}, {
				label: 'Happy',
				data: happyData,
				backgroundColor: 'rgba(255, 159, 64, 0.7)',
				borderColor: 'rgba(255, 159, 64, 1)',
				borderWidth: 1
			}, {
				label: 'Sad',
				data: sadData,
				backgroundColor: 'rgba(54, 162, 235, 0.5)',
				borderColor: 'rgba(54, 162, 235, 1)',
				borderWidth: 1
			}, {
				label: 'Surprise',
				data: surpriseData,
				backgroundColor: 'rgba(255, 205, 86, 0.5)',
				borderColor: 'rgba(255, 205, 86, 1)',
				borderWidth: 1
			}, {
				label: 'Neutral',
				data: neutralData,
				backgroundColor: 'rgba(201, 203, 207, 0.8)',
				borderColor: 'rgba(201, 203, 207, 1)',
				borderWidth: 1
			}]
		},
		options: {
			scales: {
				yAxes: [{
					ticks: {
						beginAtZero: true
					}
				}]
			}
		}
	});
}

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

function uploadVideo(vid) {
	var thumbSize = 'large',		// 設定要取得的縮圖是大圖還是小圖
		imgWidth = '200',			// 限制圖片的寬
		imgHeight = '150',			// 限制圖片的高
		address = 'https://www.youtube.com/watch?v=' + vid;
	var _type = (thumbSize == 'large') ? 0 : 2;

	try {
		// 透過youtube網址取得vid
		// var vid = address.match('[\\?&]v=([^&#]*)')[1];

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
		html += '</a><p class="col-md-6" >' + title + '</p></li>';

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
