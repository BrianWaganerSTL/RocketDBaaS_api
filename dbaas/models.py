import datetime
import textwrap

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion, CASCADE
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
import datetime
from django.utils.timezone import utc

INFINITY = timezone.datetime(9999, 12, 31, 23, 59, 59, 999999).replace(tzinfo=utc)


class DbmsTypeChoices(DjangoChoices):
    PostgreSQL = ChoiceItem()
    MongoDB = ChoiceItem()


class BackupTypeChoices(DjangoChoices):
    BackupFull = ChoiceItem("Full", "Full", 1)
    BackupIncremental = ChoiceItem("Incr","Incremental", 2)
    BackupDifferential = ChoiceItem("Diff", "Differential", 3)


class BackupStatusChoices(DjangoChoices):
    Running = ChoiceItem("Running","Running",1)
    Failed = ChoiceItem("Failed",'Failed',2)
    Successful = ChoiceItem("Successful","Successful",3)


class RestoreTypeChoices(DjangoChoices):
    RestoreFull = ChoiceItem("Full", "Restore Full", 1)
    RestoreDB = ChoiceItem("DB","Restore Database", 2)
    RestoreTable = ChoiceItem("Table", "Restore Table", 3)


class RestoreStatusChoices(DjangoChoices):
    Running = ChoiceItem("Running","Running",1)
    Failed = ChoiceItem("Failed",'Failed',2)
    Successful = ChoiceItem("Successful","Successful",3)


class ServerActivityTypeChoices(DjangoChoices):
    RestartServer = ChoiceItem("RestartServer", "Restart Server", 1)
    StopServer = ChoiceItem("StopServer", "Stop Server", 2)
    StartServer = ChoiceItem("StartServer", "Start Server", 3)
    RestartDB = ChoiceItem("RestartDB", "Restart Database", 4)
    PromoteDB = ChoiceItem("PromoteDB", "Promote Database", 5)
    DemomoteDB = ChoiceItem("DemoteDB", "Demote Database", 6)


class ServerHealthChoices(DjangoChoices):
    ServerConfiguring = ChoiceItem("ServerConfig", "Server Configuring", 1)
    ServerUp = ChoiceItem("ServerUp","Server Up and Healthy", 2)
    ServerUpWithIssues = ChoiceItem("ServerUpWithIssues","Server is Up but something is Not Healthy", 3)
    ServerDown = ChoiceItem("ServerDown", "Server is Down", 4)
    ServerOnLineMaint = ChoiceItem("ServerOnLineMaint","Server On-Line Maintenance", 5)


class ColorChoices(DjangoChoices):
    Primary = ChoiceItem("primary", "Primary", 1)
    Secondary = ChoiceItem("secondary", "Secondary", 2)
    Success = ChoiceItem("success", "Success", 3)
    Danger = ChoiceItem("danger", "Danger", 4)
    Warning = ChoiceItem("warning", "Warning", 5)
    Info = ChoiceItem("info", "Info", 6)
    Light = ChoiceItem("light", "Light", 7)
    Dark = ChoiceItem("dark", "Dark", 8)


class ActivitiesStatusChoices(DjangoChoices):
    Queued = ChoiceItem("Queued","Queued",1)
    PendingRestart = ChoiceItem("PendingRestart",'PendingRestart',2)
    Processing = ChoiceItem("Processing","Processing",3)
    Successful = ChoiceItem("Successful","Successful",4)
    Failed = ChoiceItem("Failed","Failed", 5)


class Environment(Model):
    class Meta:
        db_table = "environment"

    env_name = CharField(max_length=10, null=False, default='', primary_key=True)
    order = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=1, unique=True)


class DataCenter(Model):
    class Meta:
        db_table = "data_center"

    environment = ForeignKey(Environment, on_delete=deletion.CASCADE, null=False, default='')
    data_center = CharField(max_length=15, null=False, default='', primary_key=True)
    order = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], unique=True)


class PoolServer(Model):
    class Meta:
        db_table = "pool_server"

    class StatusInPoolChoices(DjangoChoices):
        Available = ChoiceItem("Available", "Available",1)
        Locked = ChoiceItem("Locked", "Locked for Build",2)
        Used = ChoiceItem("Used", "Used",3)

    environment = ForeignKey(Environment, on_delete=deletion.CASCADE, null=False, default='')
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    dbms_type = CharField(max_length=10, null=False, default='', choices=DbmsTypeChoices.choices)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    ram_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = ForeignKey(DataCenter, on_delete=deletion.CASCADE, null=False, default='')
    status_in_pool = CharField(max_length=20, null=False, default='', choices=StatusInPoolChoices.choices)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ServerPort(Model):
    class Meta:
        db_table = "server_port"

    class PortStatusChoices(DjangoChoices):
        Free = ChoiceItem("Free", "Free", 1)
        Locked = ChoiceItem("Locked", "Locked", 2)
        Used = ChoiceItem("Used", "Used", 3)
        Hidden = ChoiceItem("Hidden", "Hidden", 4)

    def __str__(self):
        return str(self.port)

    port = IntegerField(validators=[MinValueValidator(1024), MaxValueValidator(65535)], primary_key=True, unique=True)
    port_status = CharField(max_length=10, choices=PortStatusChoices.choices, null=False, default='Free')
    port_notes = CharField(max_length=100, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)

    def NextOpenPort(self):
        serverPort__LastUsed = ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.Used).last()
        serverPort__NextPort = ServerPort.objects.filter(port__gt=serverPort__LastUsed.port).filter(port_status=ServerPort.PortStatusChoices.Free).first()
        return serverPort__NextPort.pk


class Contact(Model):
    class Meta:
        db_table = "contact"

    class ContactTypeChoices(DjangoChoices):
        Person = ChoiceItem("Person","Person",1)
        Group = ChoiceItem("Distro","Email Group Distro",2)
        API = ChoiceItem("API","API Endpoint",3)

    contact_name = CharField(max_length=60, unique=True, null=False)
    contact_type = CharField(max_length=30, choices=ContactTypeChoices.choices, null=False, default='')
    contact_email = EmailField(null=False, default='default@email.com')
    contact_phone = CharField(max_length=15)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_name


class Application(Model):
    class Meta:
        db_table = "application"

    def __str__(self):
        return self.application_name

    application_name = CharField(max_length=40, unique=True, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True)


class Cluster(Model):
    class Meta:
        db_table = "cluster"

    def __str__(self):
        return self.cluster_name


    class ClusterHealthChoices(DjangoChoices):
        ClusterConfiguring = ChoiceItem("ClusterConfig", "Cluster Configuring", 1)
        ClusterUp = ChoiceItem("ClusterUp","Nodes Up and Healthy", 2)
        ClusterUpWithIssues = ChoiceItem("ClusterUpWithIssues","Primary is Up but something is Not Healthy", 3)
        ClusterDown = ChoiceItem("ClusterDown", "Cluster is Down", 4)
        ClusterOnLineMaint = ChoiceItem("ClusterOnLineMaint","On-Line Maintenance", 5)

    cluster_name = CharField(max_length=30, unique=True, null=False)
    dbms_type = CharField(choices=DbmsTypeChoices.choices, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.CASCADE, null=False)
    environment = ForeignKey(Environment, on_delete=deletion.PROTECT, null=False)
    requested_cpu = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(14)], null=False, default=0)
    requested_ram_gb = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(64)], null=False, default=0)
    requested_db_gb = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(102400)], null=False, default=0)
    read_write_port = ForeignKey(ServerPort, on_delete=deletion.ProtectedError, null=False, default=65535, related_name='read_write_port_id')
    read_only_port = ForeignKey(ServerPort, on_delete=deletion.ProtectedError, null=False, default=65535, related_name='read_only_port_id')
    tls_enabled_sw = BooleanField(null=False, default=True)
    backup_retention_days = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], null=False, default=14)
    cluster_health = CharField(max_length=30, null=False, choices=ClusterHealthChoices.choices, default=ClusterHealthChoices.ClusterConfiguring)
    active_sw = BooleanField(null=False, default=True)
    eff_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    exp_dttm = DateTimeField(null=False, default=INFINITY)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class Server(Model):
    class Meta:
        db_table="server"

    def __str__(self):
        return self.server_name

    class NodeRoleChoices(DjangoChoices):
        Primary = ChoiceItem("Primary", "Primary Node",1)
        SecondarySync = ChoiceItem("SecondarySync", "Secondary Node - Replication is Synchronous",2)
        SecondaryAsync = ChoiceItem("SecondaryAsync", "Secondary Node- Replication is Asynchronous",3)
        Arbiter = ChoiceItem("Arbiter", "Arbiter Node",4)

    cluster = ForeignKey(Cluster, related_name='clusters', on_delete=deletion.CASCADE, null=False)
    environment = ForeignKey(Environment, on_delete=deletion.CASCADE, null=False, default='SBX')
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    ram_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = ForeignKey(DataCenter, on_delete=deletion.CASCADE, null=False, default='')
    node_role = CharField(choices=NodeRoleChoices.choices, max_length=20, null=False, default='')
    server_health = CharField(choices=ServerHealthChoices.choices, max_length=20, null=False, default='')
    os_version = CharField(max_length=30)
    db_version = CharField(max_length=30)
    pending_restart_sw = BooleanField(null=False, default=False)
    metrics_sw = BooleanField(null=False, default=True)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class ApplicationContact(Model):
    class Meta:
        db_table = "application_contact"

    application = ForeignKey(Application, on_delete=deletion.CASCADE, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.CASCADE, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class Backup (models.Model):
    class Meta:
        db_table = "backup"
        ordering = ['start_dttm']

    cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False)
    backup_type = CharField(max_length=10, null=False, choices=BackupTypeChoices.choices, default=BackupTypeChoices.BackupFull)
    backup_status = CharField(max_length=15, choices=BackupStatusChoices.choices)
    db_size_gb = DecimalField(decimal_places=2, max_digits=5, null=False, default=0)
    backup_size_gb = DecimalField(decimal_places=2, max_digits=5, null=False, default=0)
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    stop_dttm = DateTimeField(editable=True, default=INFINITY)
    deleted_dttm = DateTimeField(editable=True, default=INFINITY)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    @property
    def _duration(self):
        return self.stop_dttm-self.start_dttm
    duration = property(_duration)

    @property
    def _deleted_sw(self):
        return (self.deleted_dttm < datetime.date.now())
    deleted_sw = property(_deleted_sw)


class Restore(models.Model):
    class Meta:
        db_table="restore"

    from_cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False, related_name='restore_from_cluster')
    to_cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False, related_name='restore_to_cluster')
    restore_type = CharField(max_length=10, null=False, default='', choices=RestoreTypeChoices.choices)
    restore_to_dttm = DateTimeField(editable=True)
    restore_status = CharField(max_length=15, choices=RestoreStatusChoices.choices)
    restore_by = CharField(max_length=30, null=False, default='')
    ticket = CharField(max_length=30, null=False, default='')
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    stop_dttm = DateTimeField(editable=True, default=INFINITY)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def duration(self):
        return self.stop_dttm-self.start_dttm

class ServerActivity(models.Model):
    class Meta:
        db_table = "server_activities"
        ordering = ['created_dttm']

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    server_activity = CharField(max_length=20, null=False, choices=ServerActivityTypeChoices.choices,
                                default=ServerActivityTypeChoices.RestartDB)
    activity_status = CharField(max_length=15, null=False, default='Queued', choices=ActivitiesStatusChoices.choices)
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    stop_dttm = DateTimeField(editable=True, null=False, default=INFINITY)
    activity_by = CharField(max_length=30, null=False, default='')
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ClusterNote(models.Model):
    class Meta:
        db_table = "cluster_note"
        ordering = ['created_dttm']

    cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False)
    title = CharField(max_length=50)
    note = CharField(max_length=2048)
    ticket = CharField(max_length=30, null=False, default='')
    created_by = CharField(max_length=30, null=False, default='')
    note_color = CharField(max_length=15, null=False, default='', choices=ColorChoices.choices)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def shortNote(self):
        return textwrap.shorten(self.note, width=100, placeholder="...")

    def prettyNoteCreateDate(self):
        return self.created_dttm.strftime('%b %e, %Y')

# =========================================================================================
#      Create AUTH TOKEN
# =========================================================================================
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
