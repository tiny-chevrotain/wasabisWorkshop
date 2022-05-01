# Generated by Django 4.0.3 on 2022-04-30 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workshop', '0009_artist_song_artists'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='image_300_url',
            field=models.CharField(default='https://i.scdn.co/image/ab67616d00001e0262fad74218294c98e510c1c8', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='image_640_url',
            field=models.CharField(default='https://i.scdn.co/image/ab67616d0000b27362fad74218294c98e510c1c8', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='image_64_url',
            field=models.CharField(default='https://i.scdn.co/image/ab67616d0000485162fad74218294c98e510c1c8', max_length=64),
            preserve_default=False,
        ),
    ]
