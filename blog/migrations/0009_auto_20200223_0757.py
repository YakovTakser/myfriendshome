# Generated by Django 3.0.3 on 2020-02-23 05:57

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200223_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 23, 5, 57, 25, 145923, tzinfo=utc)),
        ),
    ]