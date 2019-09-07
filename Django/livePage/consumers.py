from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .recognition import emotionRecognition
import json
import cv2
import numpy as np

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['streamerName']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

class ImageConsumer(WebsocketConsumer):
    er = emotionRecognition()

    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, bytes_data):
        # convert blob to numpy byte array
        data = np.asarray(bytearray(bytes_data), dtype="uint8")
        # get grayscale image by decoding numpy byte array
        grayImage = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)

        # whether server return marked picture
        self.er.SetIsShow(True)

        # base64 of marked picture
        base64 = self.er.detect(grayImage)
        if base64 != None:
            self.send(bytes_data=base64)
