# Generated by Django 3.2 on 2021-06-29 13:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0011_auto_20210629_1333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='season',
        ),
    ]
