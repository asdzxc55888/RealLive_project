from livePage.models import EmotionData, VideoRecord
from random import randrange
import math

# declare time data, unit is seconds
start = 1
end = 3601

# declare emotion data randrange
range = 10

# initial data
angry = randrange(range) + 1
disgust = randrange(range) + 1
fear = randrange(range) + 1
happy = randrange(range) + 1
sad = randrange(range) + 1
surprise = randrange(range) + 1

# declare vid
vid = VideoRecord.objects.get(vid="ZdQvQWMRFnw")

while start <= end:
	hour = int(start / 3600)
	minute = int((start - hour * 3600) / 60)
	second = int(start - hour * 3600 - minute * 60)
	time = str(hour) + ":" + str(minute) + ":" + str(second)

	# increase or decrease one time every loop
	angry = angry + int(math.pow(-1, randrange(range)))
	disgust = angry + int(math.pow(-1, randrange(range)))
	fear = fear + int(math.pow(-1, randrange(range)))
	happy = happy + int(math.pow(-1, randrange(range)))
	sad = sad + int(math.pow(-1, randrange(range)))
	surprise = surprise + int(math.pow(-1, randrange(range)))

	# let count more than 0
	if (angry <= 0): angry = randrange(range) + 1
	if (disgust <= 0): disgust = randrange(range) + 1
	if (fear <= 0): fear = randrange(range) + 1
	if (happy <= 0): happy = randrange(range) + 1
	if (sad <= 0): sad = randrange(range) + 1
	if (surprise <= 0): surprise = randrange(range) + 1

	EmotionData.objects.create(vid=vid, Angry=angry, Disgust=disgust, Fear=fear, Happy=happy, Sad=sad, Surprise=surprise, time=time)
	start+=1
