# Generated by Django 3.0.3 on 2020-03-31 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20200331_0725'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='description',
            new_name='about',
        ),
    ]
