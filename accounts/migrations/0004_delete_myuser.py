# Generated by Django 3.0.3 on 2020-02-25 19:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('blog', '0021_auto_20200225_2125'),
        ('accounts', '0003_myuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MyUser',
        ),
    ]
