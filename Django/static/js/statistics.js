// 製作圖表
var emotion = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'];

var ctx = document.getElementById('myChart');
var myChart = new Chart(ctx, {
	type: 'bar',
	data: {
		labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
		datasets: [{
			label: '# of Votes',
			data: [12, 19, 3, 5, 2, 3],
			backgroundColor: [
				'rgba(255, 99, 132, 0.2)',
				'rgba(54, 162, 235, 0.2)',
				'rgba(255, 206, 86, 0.2)',
				'rgba(75, 192, 192, 0.2)',
				'rgba(153, 102, 255, 0.2)',
				'rgba(255, 159, 64, 0.2)'
			],
			borderColor: [
				'rgba(255, 99, 132, 1)',
				'rgba(54, 162, 235, 1)',
				'rgba(255, 206, 86, 1)',
				'rgba(75, 192, 192, 1)',
				'rgba(153, 102, 255, 1)',
				'rgba(255, 159, 64, 1)'
			],
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

function htmlToElement(html) {
    var template = document.createElement('template');
    html = html.trim();
    template.innerHTML = html;
    return template.content.firstChild;
}

// playerlist
$(function(){
	var thumbSize = 'large',		// 設定要取得的縮圖是大圖還是小圖
		imgWidth = '200',			// 限制圖片的寬
		imgHeight = '150',			// 限制圖片的高
		apiKey = 'AIzaSyBmta_M-BHZ6UixGn7HsI5owf--BBS-6-0';

	$('.connect_button').click(function(){
		var address = prompt("請輸入網址\n(ex. https://www.youtube.com/watch?v=[your video ID])", "");
		var _type = (thumbSize == 'large') ? 0 : 2;

		try {
			// 取得 vid
			var vid = address.match('[\\?&]v=([^&#]*)')[1];

			// 取得 title
			var title = 'None';
			$.ajax({
		        url: 'https://www.googleapis.com/youtube/v3/videos?part=snippet&id=' + vid + '&key=' + apiKey,
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
				// 當點擊到圖片時就轉換成 YouTube 影片
				$('#player').attr('src', 'https://www.youtube.com/embed/' + vid + '?rel=0&autoplay=1');

				return false;
			});

			$('.playlist').append(option);
		}
		catch {
			alert('網址無法連接');
		};
	});
});
