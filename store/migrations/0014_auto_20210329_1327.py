# Generated by Django 3.1.6 on 2021-03-29 13:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_auto_20210329_1325'),
    ]

    operations = [
        migrations.RenameField(
            model_name='storewallpaper',
            old_name='avatar',
            new_name='wallpaper',
        ),
    ]