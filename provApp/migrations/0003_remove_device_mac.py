# Generated by Django 3.0.3 on 2021-03-20 15:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provApp', '0002_auto_20210320_1654'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='mac',
        ),
    ]
