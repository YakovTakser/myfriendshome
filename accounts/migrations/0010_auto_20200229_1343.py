# Generated by Django 3.0.3 on 2020-02-29 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200229_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_pics/default_profile.jpg', upload_to='profile_pics/'),
        ),
    ]