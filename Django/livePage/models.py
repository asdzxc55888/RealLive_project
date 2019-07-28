from django.db import models
from django.conf import settings

# Create your models here.
class UserSetting(models.Model):
    introduction = models.CharField(max_length=1200, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    youtubeUrl = models.CharField(max_length=100, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    nickName = models.CharField(max_length=20, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    userId = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, default = "")


    #每一筆資料在管理介面顯示的內容以下列程式定義
    def __str__(self):
        return self.nickName #表示顯示cName欄位


class EmotionData(models.Model):
    vid = models.CharField(max_length = 20, null = False)
    time = models.TimeField(null = False)
    Angry = models.PositiveIntegerField(default = 0)
    Disgust = models.PositiveIntegerField(default = 0)
    Fear = models.PositiveIntegerField(default = 0)
    Happy = models.PositiveIntegerField(default = 0)
    Sad = models.PositiveIntegerField(default = 0)
    Surprise = models.PositiveIntegerField(default = 0)
    Neutral = models.PositiveIntegerField(default = 0)
