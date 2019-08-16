from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.models import User
from .models import UserSetting
from Django.settings import BASE_DIR
from keras.models import load_model
import cv2
import numpy as np
import time

# Create your views here.
class liveView(View):
    template_name = 'live.html'

    def get(self, request, streamerName, *args, **kwargs):
        streamer = get_object_or_404(User, username = streamerName)
        streamerSettingData = UserSetting.objects.get(userId = streamer.id)
        context = {
            "youtubeUrl": streamerSettingData.youtubeUrl,
        }
        return render(request, self.template_name, context)

def preprocess_input(x, v2=True):
    x = x.astype('float32') # int to float
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x

def detect(request, streamerName):
    emotionLabels = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

    # offset of emotional picture. enlarging picture in order to cover all face
    x_offset = 20
    y_offset = 40

    # trained models address
    detectionModelPath = BASE_DIR + '/trainedModel/detectionModels/haarcascade_frontalface_default.xml'
    emotionModelPath = BASE_DIR + '/trainedModel/emotionModels/fer2013_mini_XCEPTION.102-0.66.hdf5'

    # loading models
    faceDetection = cv2.CascadeClassifier(detectionModelPath)
    emotionClassifier = load_model(emotionModelPath, compile=False)

    # getting input model shapes for inference, 64 * 64 array
    emotionTargetSize = emotionClassifier.input_shape[1:3]

    # recording emotion
    records = { 'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0 }

    cam = cv2.VideoCapture(0)
    t = time.time()

    while True:
        if time.time() - t >= 1.0:
            t = time.time()

            # load image
            bgr_image = cam.read()[1]
            gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

            # detecting faces location
            faces = faceDetection.detectMultiScale(gray_image, 1.3, 5)

            for(x,y,w,h) in faces:
                # show rectangle for test
                cv2.rectangle(bgr_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # get gray face image
                x1, x2, y1, y2 = (x - x_offset, x + w + x_offset, y - y_offset, y + h + y_offset)
                grayFace = gray_image[y1:y2, x1:x2]

                try:
                    # compressing original picture size to 64 * 64
                    grayFace = cv2.resize(grayFace, (emotionTargetSize))
                except:
                    continue

                # changing grayFace to float32 and doing some calculation
                grayFace = preprocess_input(grayFace, True)
                # inserting a dimension at head
                grayFace = np.expand_dims(grayFace, 0)
                # appending a dimension at tail
                grayFace = np.expand_dims(grayFace, -1)

                emotionPrediction = emotionClassifier.predict(grayFace)

                # get the biggest number of prediction
                emotionProbability = np.max(emotionPrediction)
                # get index of the biggest number
                emotionLabelArg = np.argmax(emotionPrediction)
                # get corresponding emotion
                emotionText = emotionLabels[emotionLabelArg]
                print(emotionText)

                records[emotionText] += 1

            # show windows for test
            cv2.imshow("Face",bgr_image)

        if(cv2.waitKey(1) == ord('q')):
            cam.release()
            cv2.destroyAllWindows()
            break

    return redirect('/')
