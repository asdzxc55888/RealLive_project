from django.contrib import admin

# Register your models here.
from livePage.models import UserSetting, EmotionData, VideoRecord, ChatRecord

admin.site.register(UserSetting)
admin.site.register(EmotionData)
admin.site.register(VideoRecord)
admin.site.register(ChatRecord)
