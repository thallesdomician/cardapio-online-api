# Generated by Django 3.1.6 on 2021-02-14 05:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='city',
            name='active',
        ),
        migrations.RemoveField(
            model_name='city',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='city',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='city',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='state',
            name='active',
        ),
        migrations.RemoveField(
            model_name='state',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='state',
            name='deleted_at',
        ),
        migrations.RemoveField(
            model_name='state',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='address',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]