# Generated by Django 2.1.4 on 2019-01-02 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0006_server_dbms_type'),
        ('metrics', '0005_auto_20181231_0007'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Metrics_HostDetails',
            new_name='Metrics_HostDetail',
        ),
    ]
