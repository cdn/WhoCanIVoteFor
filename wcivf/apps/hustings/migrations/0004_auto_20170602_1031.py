# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-02 10:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hustings', '0003_husting_video_url'),
    ]

    operations = [
        migrations.RenameField(
            model_name='husting',
            old_name='video_url',
            new_name='postevent_url',
        ),
    ]