# Generated by Django 3.0.3 on 2021-03-20 18:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provApp', '0014_auto_20210320_1928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dss',
            name='extension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Extension', to='provApp.Extension'),
        ),
    ]