# Generated by Django 2.1.1 on 2018-10-03 03:36

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dbaas', '0007_auto_20180930_1506'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServerPorts',
            fields=[
                ('port', models.IntegerField(primary_key=True, serialize=False, validators=[django.core.validators.MinValueValidator(1024), django.core.validators.MaxValueValidator(65535)])),
                ('port_status', models.CharField(choices=[('Free', 'Free'), ('Used', 'Used'), ('Hidden', 'Hidden')], max_length=10, null=True)),
                ('port_notes', models.CharField(max_length=100)),
                ('updated_dttm', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'server_ports',
            },
        ),
        migrations.AddField(
            model_name='cluster',
            name='read_only_port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.ProtectedError, related_name='read_only_port_id', to='dbaas.Application'),
        ),
        migrations.AddField(
            model_name='server',
            name='server_health',
            field=models.CharField(blank=True, choices=[('ServerConfig', 'Server Configuring'), ('ServerUp', 'Server Up and Healthy'), ('ServerUpWithIssues', 'Server is Up but something is Not Healthy'), ('ServerDown', 'Server is Down'), ('ServerOnLineMaint', 'Server On-Line Maintenance')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='serveractivities',
            name='server_activity',
            field=models.CharField(choices=[('RestartServer', 'Restart Server'), ('StopServer', 'Stop Server'), ('StartServer', 'Start Server'), ('RestartDB', 'Restart Database'), ('PromoteDB', 'Promote Database'), ('DemoteDB', 'Demote Database')], default='RestartDB', max_length=20),
        ),
        migrations.AddField(
            model_name='cluster',
            name='read_write_port',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.ProtectedError, related_name='read_write_port_id', to='dbaas.ServerPorts'),
        ),
    ]
