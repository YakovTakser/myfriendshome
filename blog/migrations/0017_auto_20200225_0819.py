# Generated by Django 3.0.3 on 2020-02-25 06:19

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0016_auto_20200225_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 25, 6, 19, 49, 760465, tzinfo=utc)),
        ),
    ]