# Generated by Django 3.0.3 on 2021-03-20 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('provApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='device',
            old_name='MAC',
            new_name='mac',
        ),
    ]
