# Generated by Django 3.1.6 on 2021-02-19 03:13

from django.db import migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20210218_0120'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='store',
            name='logo',
        ),
        migrations.RemoveField(
            model_name='store',
            name='thumbnail',
        ),
        migrations.AddField(
            model_name='store',
            name='image',
            field=sorl.thumbnail.fields.ImageField(blank=True, null=True, upload_to='store'),
        ),
    ]