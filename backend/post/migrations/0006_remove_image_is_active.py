# Generated by Django 2.2.13 on 2020-07-03 08:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0005_auto_20200703_0411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='is_active',
        ),
    ]
