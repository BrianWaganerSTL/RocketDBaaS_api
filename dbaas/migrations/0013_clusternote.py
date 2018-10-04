# Generated by Django 2.1.1 on 2018-10-04 03:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0012_auto_20181002_2312'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('note', models.CharField(max_length=2048)),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('updated_dttm', models.DateTimeField(auto_now=True)),
                ('cluster', models.ForeignKey(null=True, on_delete=django.db.models.deletion.ProtectedError, to='dbaas.Cluster')),
            ],
            options={
                'db_table': 'cluster_note',
            },
        ),
    ]
