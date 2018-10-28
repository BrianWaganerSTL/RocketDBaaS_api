# Generated by Django 2.1.1 on 2018-10-25 22:20

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0028_auto_20181025_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serveractivities',
            name='activity_status',
            field=models.CharField(choices=[('Queued', 'Queued'), ('PendingRestart', 'PendingRestart'), ('Processing', 'Processing'), ('Failed', 'Failed'), ('Successful', 'Successful')], default='Queued', max_length=15),
        ),
        # migrations.AlterField(
        #     model_name='serveractivities',
        #     name='start_dttm',
        #     field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        # ),
        # migrations.AlterField(
        #     model_name='serveractivities',
        #     name='stop_dttm',
        #     field=models.DateTimeField(default=datetime.datetime(9999, 12, 31, 23, 59, 59, 999999, tzinfo=utc)),
        # ),
        # migrations.AlterField(
        #     model_name='serverport',
        #     name='port_notes',
        #     field=models.CharField(default='', max_length=100),
        # ),
    ]
