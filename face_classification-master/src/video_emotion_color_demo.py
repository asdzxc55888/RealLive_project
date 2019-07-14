from statistics import mode

import cv2
from keras.models import load_model
import numpy as np

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
#
import matplotlib.pyplot as plt
import time
#

# parameters for loading data and images
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013') #返回情緒種類的dic

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models ，return CascadeClassifier
face_detection = load_detection_model(detection_model_path) #載入臉部辨識資料模組
emotion_classifier = load_model(emotion_model_path, compile=False) #載入臉部情緒資料

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3] #(64, 64)的矩陣

# starting lists for calculating modes
emotion_window = [] #存放情緒文字 ex:happy,sad

# starting video streaming
cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(0) #開啟鏡頭 VideoCapture(int device) device為裝置編號

# recording emotion
records = { 'angry': 0, 'disgust': 0, 'fear': 0, 'happy': 0, 'sad': 0, 'surprise': 0, 'neutral': 0 } # 每個情緒總共出現幾個clockz
#
while True:
    bgr_image = video_capture.read()[1] #讀取鏡頭影像
    gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY) #彩色轉灰
    rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB) #B,R互換
    faces = detect_faces(face_detection, gray_image) #模組與鏡頭對照搜尋臉部座標

    for face_coordinates in faces:  #把搜尋到的臉部座標輸出(n,3)

        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets) #人臉情感檢測，放大臉部範圍
        gray_face = gray_image[y1:y2, x1:x2]

        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size)) #縮小原圖大小
        except:
            continue

        gray_face = preprocess_input(gray_face, True) #把gray_face轉乘float32，並運算
        gray_face = np.expand_dims(gray_face, 0) #在頭插入一維
        gray_face = np.expand_dims(gray_face, -1) #在尾插入一維

        emotion_prediction = emotion_classifier.predict(gray_face) #與dataset做臉部情緒預測

        emotion_probability = np.max(emotion_prediction) #取出emotion_prediction陣列中最大的值
        emotion_label_arg = np.argmax(emotion_prediction) #取出emotion_prediction陣列中最大值的索引值
        emotion_text = emotion_labels[emotion_label_arg] #輸出權值最大所對應的情緒分析
        emotion_window.append(emotion_text) #在陣列最後加入一個情緒字串 ex:sad,happy

        if len(emotion_window) > frame_window: #陣列中長度大於10，pop出index(0)的值
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window) #找出陣列中最常出現的情緒字串
        except:
            continue
#
        records[emotion_text] += 1
#
        if emotion_text == 'angry':
            color = emotion_probability * np.asarray((255, 0, 0)) #權值越高顏色越明顯
        elif emotion_text == 'disgust':
            color = emotion_probability * np.asarray((0, 255, 0))
        elif emotion_text == 'fear':
            color = emotion_probability * np.asarray((128, 0, 128))
        elif emotion_text == 'happy':
            color = emotion_probability * np.asarray((255, 255, 0))
        elif emotion_text == 'sad':
            color = emotion_probability * np.asarray((0, 0, 255))
        elif emotion_text == 'surprise':
            color = emotion_probability * np.asarray((0, 255, 255))
        elif emotion_text == 'neutral':
            color = emotion_probability * np.asarray((0, 0, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color) #劃出框框
        draw_text(face_coordinates, rgb_image, emotion_text, color, 0, -45, 1, 1) #顯示文字

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image) #以RGB畫面秀出

    if cv2.waitKey(1) & 0xFF == ord('q'):
        video_capture.release()
        cv2.destroyAllWindows()
        break
#
plt.bar(range(len(records)), list(records.values()), align = 'center')
plt.xticks(range(len(records)), list(records.keys()))
plt.show()
#
