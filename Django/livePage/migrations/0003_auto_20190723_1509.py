# Generated by Django 2.2 on 2019-07-23 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livePage', '0002_auto_20190723_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotiondata',
            name='time',
            field=models.TimeField(null=True),
        ),
    ]