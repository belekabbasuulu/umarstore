# Generated by Django 3.2 on 2021-06-29 13:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0013_auto_20210629_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='season',
            name='slug',
        ),
    ]
