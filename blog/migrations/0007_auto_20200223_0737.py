# Generated by Django 3.0.3 on 2020-02-23 05:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20200222_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2020, 2, 23, 5, 37, 5, 773993, tzinfo=utc)),
        ),
    ]
