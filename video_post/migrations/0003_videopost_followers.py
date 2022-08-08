# Generated by Django 4.0.6 on 2022-08-04 12:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('video_post', '0002_videopost_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='videopost',
            name='followers',
            field=models.ManyToManyField(related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
