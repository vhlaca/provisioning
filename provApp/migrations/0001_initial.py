# Generated by Django 3.0.3 on 2021-03-20 15:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('MAC', models.CharField(max_length=12)),
            ],
        ),
        migrations.CreateModel(
            name='DevModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dss', models.BooleanField(default=False)),
                ('device_format', models.TextField(choices=[('Software telephone', 'Softphone'), ('Hardware IP telephone', 'Hardphone')], default='Software telephone', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DevVendor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='DSS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dssType', models.TextField(choices=[('BLF - Busy Lamp Field', 'Blf'), ('SPD - Speed dial key', 'Spd')], default='BLF - Busy Lamp Field', max_length=45)),
                ('key', models.IntegerField(default=1)),
                ('value', models.CharField(max_length=255)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Device', to='provApp.Device')),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='devmodel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='DeviceModel', to='provApp.DevModel'),
        ),
    ]