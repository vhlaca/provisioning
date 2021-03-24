# Generated by Django 3.0.3 on 2021-03-20 19:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('provApp', '0020_auto_20210320_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='description',
            field=models.CharField(max_length=100, verbose_name='Customer'),
        ),
        migrations.AlterField(
            model_name='device',
            name='extension',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='provApp.Extension'),
        ),
        migrations.AlterUniqueTogether(
            name='dss',
            unique_together={('key', 'device')},
        ),
    ]