# Generated by Django 2.1.1 on 2018-11-26 07:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0009_auto_20181124_0100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='note',
            field=models.CharField(default='', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='note_by',
            field=models.CharField(default='', max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='ticket',
            field=models.CharField(default='', max_length=30, null=True),
        ),
    ]
