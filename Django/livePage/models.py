from django.db import models
from django.conf import settings

# Create your models here.
class UserSetting(models.Model):
    introduction = models.CharField(max_length = 1200, null = True) #建立字串型別的欄位，最大長度為1200字元，欄位可空白
    youtubeUrl = models.CharField(max_length = 100, null = True)    #建立字串型別的欄位，最大長度為100字元，欄位可空白
    nickName = models.CharField(max_length = 20, null = False)       #建立字串型別的欄位，最大長度為20字元，欄位可空白
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default = "", null = False)
    isLive = models.BooleanField(default = "False", null = True)


    #每一筆資料在管理介面顯示的內容以下列程式定義
    def __str__(self):
        return self.nickName #表示顯示cName欄位


class EmotionData(models.Model):
    vid = models.ForeignKey('VideoRecord', on_delete = models.CASCADE, default = "")
    time = models.TimeField(null = False)
    Angry = models.PositiveIntegerField(default = 0)
    Disgust = models.PositiveIntegerField(default = 0)
    Fear = models.PositiveIntegerField(default = 0)
    Happy = models.PositiveIntegerField(default = 0)
    Sad = models.PositiveIntegerField(default = 0)
    Surprise = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return '%s %s' % (self.vid, self.time)

    # restrict that there does not exist two data with same vid and time
    class Meta:
        unique_together = ['vid', 'time']

class VideoRecord(models.Model):
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = "")
    vid = models.CharField(max_length = 20, null = False)

    def __str__(self):
        return self.vid

class ChatRecord(models.Model):
    vid = models.ForeignKey('VideoRecord', on_delete = models.CASCADE, default = "") #連接影片
    userId = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, default = "") #發送訊息的使用者
    message = models.CharField(max_length = 1200, null = True) #訊息
    date = models.DateField(auto_now_add=True, blank=True) #auto_now_add 取得當前時間
    time = models.TimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '%s %s' % (self.userId, self.message)
