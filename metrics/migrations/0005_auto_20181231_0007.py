# Generated by Django 2.1.4 on 2018-12-31 06:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('metrics', '0004_auto_20181231_0005'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='metrics_hostdetails',
            table='metrics_host_detail',
        ),
    ]