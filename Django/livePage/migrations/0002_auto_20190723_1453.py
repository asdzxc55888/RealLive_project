# Generated by Django 2.2 on 2019-07-23 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('livePage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emotiondata',
            name='Angry',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Disgust',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Fear',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Happy',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Neutral',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Sad',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='emotiondata',
            name='Surprise',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
