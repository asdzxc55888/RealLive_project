from .models import EmotionData, VideoRecord
from Django.settings import BASE_DIR
from keras.models import load_model
from keras import backend
import tensorflow as tf
import cv2
import numpy as np
import base64

class Recognizer:
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
    graph = tf.get_default_graph()

    # getting input model shapes for inference, 64 * 64 array
    emotionTargetSize = emotionClassifier.input_shape[1:3]

    isShow = False

    def SetIsShow(self, flag):
        self.isShow = flag

    def preprocessInput(self, x, v2=True):
        x = x.astype('float32') # int to float
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x

    def recognize(self, grayImage, _vid, _time):
        # get records
        v = VideoRecord.objects.get(vid = _vid)
        try:
            records = EmotionData.objects.get(vid = v, time = _time)
        except:
            records = EmotionData.objects.create(vid = v, Angry = 0, Disgust = 0, Fear = 0, Happy = 0, Sad = 0, Surprise = 0, time = _time)

        # storeing emotion type and corresponding location
        emotions = []

        # detecting faces location
        faces = self.faceDetection.detectMultiScale(grayImage, 1.3, 5)

        for (x,y,w,h) in faces:
            # get gray face image
            x1, x2, y1, y2 = (x - self.x_offset, x + w + self.x_offset, y - self.y_offset, y + h + self.y_offset)
            grayFace = grayImage[y1:y2, x1:x2]

            try:
                # compressing original picture size to 64 * 64
                grayFace = cv2.resize(grayFace, (self.emotionTargetSize))
            except:
                continue

            # changing grayFace to float32 and doing some calculation
            grayFace = self.preprocessInput(grayFace, True)
            # inserting a dimension at head
            grayFace = np.expand_dims(grayFace, 0)
            # appending a dimension at tail
            grayFace = np.expand_dims(grayFace, -1)

            with self.graph.as_default():
                emotionPrediction = self.emotionClassifier.predict(grayFace)

                # get the biggest number of prediction
                emotionProbability = np.max(emotionPrediction)
                # get index of the biggest number
                emotionLabelArg = np.argmax(emotionPrediction)
                # get corresponding emotion
                emotionText = self.emotionLabels[emotionLabelArg]

                if emotionText == 'angry':
                    records.Angry += 1
                elif emotionText == 'disgust':
                    records.Disgust += 1
                elif emotionText == 'fear':
                    records.Fear += 1
                elif emotionText == 'happy':
                    records.Happy += 1
                elif emotionText == 'sad':
                    records.Sad += 1
                elif emotionText == 'surprise':
                    records.Surprise += 1
                records.save()

                emotions.append((emotionText, x, y, w, h))

        if self.isShow:
            for (emotionText, x, y, w, h) in emotions:
                cv2.rectangle(grayImage, (x, y), (x + w, y + h), (255, 255, 255), 2)
                cv2.putText(grayImage, emotionText, (x, y - 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
            return cv2.imencode('.jpg', grayImage)[1].tostring()
        else:
            return None
