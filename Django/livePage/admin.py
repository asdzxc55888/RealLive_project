from django.contrib import admin

# Register your models here.
from livePage.models import UserSetting, EmotionData

admin.site.register(UserSetting)
admin.site.register(EmotionData)
