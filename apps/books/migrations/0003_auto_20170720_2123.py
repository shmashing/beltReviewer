# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-20 21:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20170719_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='books.Author'),
        ),
    ]
