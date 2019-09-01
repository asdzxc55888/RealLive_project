from Django.settings import BASE_DIR
from keras.models import load_model
from keras import backend
import cv2
import numpy as np

def preprocess_input(x, v2=True):
    x = x.astype('float32') # int to float
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x

def detect(grayImage):
    # clear old tensorflow session before detect
    backend.clear_session();

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

    # detecting faces location
    faces = faceDetection.detectMultiScale(grayImage, 1.3, 5)

    for (x,y,w,h) in faces:
        # get gray face image
        x1, x2, y1, y2 = (x - x_offset, x + w + x_offset, y - y_offset, y + h + y_offset)
        grayFace = grayImage[y1:y2, x1:x2]

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

    # clear tensorflow session after detect
    backend.clear_session();
