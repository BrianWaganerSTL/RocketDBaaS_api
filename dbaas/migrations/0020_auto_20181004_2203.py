# Generated by Django 2.1.1 on 2018-10-05 03:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0019_auto_20181004_2150'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='serveractivities',
            options={'ordering': ['created_dttm']},
        ),
    ]