# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-05-18 12:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0017_auto_20170518_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personpost',
            name='election',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Election'),
        ),
        migrations.AlterField(
            model_name='personpost',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='parties.Party'),
        ),
        migrations.AlterField(
            model_name='personpost',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.Person'),
        ),
        migrations.AlterField(
            model_name='personpost',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='elections.Post'),
        ),
    ]