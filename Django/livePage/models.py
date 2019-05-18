from django.db import models

# Create your models here.

class user(models.Model):
    userName = models.CharField(max_length=20, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    password = models.CharField(max_length=20, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白
    nickName = models.CharField(max_length=20, null=False) #建立字串型別的欄位，最大長度為20字元，欄位不可空白


    #每一筆資料在管理介面顯示的內容以下列程式定義
    def __str__(self):
        return self.userName #表示顯示cName欄位