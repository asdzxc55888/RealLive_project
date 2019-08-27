from livePage.models import EmotionData, VideoRecord
from random import randrange

# declare time data, unit is seconds
start = 3601
end = 3601

# declare emotion data randrange
range = 10

# declare vid
vid = VideoRecord.objects.get(vid="-oQvMHpKkms")

while start <= end:
	hour = int(start / 3600)
	minute = int((start - hour * 3600) / 60)
	second = int(start - hour * 3600 - minute * 60)
	time = str(hour) + ":" + str(minute) + ":" + str(second)
	EmotionData.objects.create(vid=vid, Angry=randrange(range), Disgust=randrange(range), Fear=randrange(range), Happy=randrange(range), Sad=randrange(range), Surprise=randrange(range), time=time)
	start+=1
