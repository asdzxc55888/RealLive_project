# Generated by Django 2.2 on 2019-09-18 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livePage', '0007_usersetting_islive'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersetting',
            name='category',
            field=models.CharField(default='Unknown', max_length=20),
        ),
        migrations.AlterField(
            model_name='usersetting',
            name='nickName',
            field=models.CharField(default='Newcomer', max_length=20),
        ),
    ]
