# Generated by Django 3.2 on 2021-06-22 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_auto_20210622_0336'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='season',
            field=models.CharField(max_length=100, null=True),
        ),
    ]