# Generated by Django 2.1.4 on 2018-12-31 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0003_auto_20181230_1550'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='last_reboot',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]