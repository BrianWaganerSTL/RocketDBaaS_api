import datetime
import textwrap

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.timezone import utc
from djchoices import DjangoChoices, ChoiceItem
from rest_framework.authtoken.models import Token

INFINITY = timezone.datetime(9999, 12, 31, 23, 59, 59, 999999).replace(tzinfo=utc)


class DbmsTypeChoices(DjangoChoices):
    PostgreSQL = ChoiceItem()
    MongoDB = ChoiceItem()


class ColorChoices(DjangoChoices):
    PRIMARY = ChoiceItem("primary", "Primary", 1)
    SECONDARY = ChoiceItem("secondary", "Secondary", 2)
    SUCCESS = ChoiceItem("success", "Success", 3)
    DANGER = ChoiceItem("danger", "Danger", 4)
    WARNING = ChoiceItem("warning", "Warning", 5)
    INFO = ChoiceItem("info", "Info", 6)
    LIGHT = ChoiceItem("light", "Light", 7)
    DARK = ChoiceItem("dark", "Dark", 8)


class Environment(Model):
    class Meta:
        db_table = "dbaas_environment"
        ordering = ['order_num']

    def __str__(self):
        return self.env_name

    env_name = CharField(max_length=10, null=False, default='', primary_key=True, unique=True)
    order_num = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=1, unique=True)


class Datacenter(Model):
    class Meta:
        db_table = "dbaas_datacenter"
        ordering = ['order_num']

    def __str__(self):
        return self.datacenter

    datacenter = CharField(max_length=15, null=False, default='', unique=True)
    order_num = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(99)], default=1, unique=True)


class ServerPort(Model):
    class Meta:
        db_table = "dbaas_server_port"

    class PortStatusChoices(DjangoChoices):
        FREE = ChoiceItem("Free", "Free", 1)
        LOCKED = ChoiceItem("Locked", "Locked", 2)
        USED = ChoiceItem("Used", "Used", 3)
        HIDDEN = ChoiceItem("Hidden", "Hidden", 4)

    def __str__(self):
        return str(self.port)

    port = IntegerField(validators=[MinValueValidator(1024), MaxValueValidator(65535)], primary_key=True, unique=True)
    port_status = CharField(max_length=10, choices=PortStatusChoices.choices, null=False, default=PortStatusChoices.FREE)
    port_notes = CharField(max_length=100, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)

    def NextOpenPort(self):
        cnt = ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.USED).count()
        if (cnt == 0):
            serverPort__NextPort = ServerPort.objects.filter(port__gt=1023).filter(port_status=ServerPort.PortStatusChoices.FREE).first()
        else:
            serverPort__LastUsed = ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.USED).last()
            serverPort__NextPort = ServerPort.objects.filter(port__gt=serverPort__LastUsed).filter(port_status=ServerPort.PortStatusChoices.FREE).first()

        return serverPort__NextPort


class Contact(Model):
    class Meta:
        db_table = "dbaas_contact"

    class ContactTypeChoices(DjangoChoices):
        PERSON = ChoiceItem("Person", "Person", 1)
        GROUP = ChoiceItem("Distro", "Email Group Distro", 2)
        API = ChoiceItem("API","API Endpoint",3)

    contact_name = CharField(max_length=60, unique=True, null=False)
    contact_type = CharField(max_length=30, choices=ContactTypeChoices.choices, null=False, default=ContactTypeChoices.PERSON)
    contact_email = EmailField(null=False, default='default@email.com')
    contact_phone = CharField(max_length=15, null=True, blank=True)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_name


class Application(Model):
    class Meta:
        db_table = "dbaas_application"

    # def __str__(self):
    #     return self.application_name

    application_name = CharField(max_length=40, unique=True, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True)


class Cluster(Model):
    class Meta:
        db_table = "dbaas_cluster"

    def __str__(self):
        return self.cluster_name


    class ClusterHealthChoices(DjangoChoices):
        CLUSTERCONFIGURING = ChoiceItem("ClusterConfig", "Cluster Configuring", 1)
        CLUSTERUP = ChoiceItem("ClusterUp", "Nodes Up and Healthy", 2)
        CLUSTERUPWITHISSUES = ChoiceItem("ClusterUpWithIssues", "Primary is Up but something is Not Healthy", 3)
        CLUSTERDOWN = ChoiceItem("ClusterDown", "Cluster is Down", 4)
        CLUSTERONLINEMAINT = ChoiceItem("ClusterOnLineMaint", "On-Line Maintenance", 5)

    cluster_name = CharField(max_length=30, unique=True, null=False)
    dbms_type = CharField(choices=DbmsTypeChoices.choices, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.CASCADE, null=False)
    environment = ForeignKey(Environment, on_delete=deletion.PROTECT, null=False)
    read_write_port = ForeignKey(ServerPort, on_delete=deletion.ProtectedError, null=False, default=65535, related_name='read_write_port_id')
    read_only_port = ForeignKey(ServerPort, on_delete=deletion.ProtectedError, null=False, default=65535, related_name='read_only_port_id')
    tls_enabled_sw = BooleanField(null=False, default=True)
    backup_retention_days = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], null=False, default=14)
    cluster_health = CharField(max_length=30, null=False, choices=ClusterHealthChoices.choices, default=ClusterHealthChoices.CLUSTERCONFIGURING)
    active_sw = BooleanField(null=False, default=True)
    eff_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    exp_dttm = DateTimeField(null=True, blank=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class Server(Model):
    class Meta:
        db_table="dbaas_server"

    def __str__(self):
        return self.server_name

    class NodeRoleChoices(DjangoChoices):
        CONFIGURING = ChoiceItem("Configuring", "Primary Configuring", 1)
        PRIMARY = ChoiceItem("Primary", "Primary Node", 2)
        SECONDARYSYNC = ChoiceItem("SecondarySync", "Secondary Node - Replication is Synchronous", 3)
        SECONDARYASYNC = ChoiceItem("SecondaryAsync", "Secondary Node- Replication is Asynchronous", 4)
        ARBITER = ChoiceItem("Arbiter", "Arbiter Node", 5)
        POOLSERVER = ChoiceItem("PoolServer", "PoolServer", 6)
        POOLSERVERLOCKED = ChoiceItem("PoolServerLocked", "PoolServerLocked", 7)

    class ServerHealthChoices(DjangoChoices):
        SERVERCONFIGURING = ChoiceItem("ServerConfig", "Server Configuring", 1)
        SERVERUP = ChoiceItem("ServerUp", "Server Up and Healthy", 2)
        SERVERUPWITHISSUES = ChoiceItem("ServerUpWithIssues", "Server is Up but something is Not Healthy", 3)
        SERVERDOWN = ChoiceItem("ServerDown", "Server is Down", 4)
        SERVERONLINEMAINT = ChoiceItem("ServerOnLineMaint", "Server On-Line Maintenance", 5)

    cluster = ForeignKey(Cluster, related_name='clusters', on_delete=deletion.CASCADE, null=True, blank=True)
    environment = ForeignKey(Environment, on_delete=deletion.CASCADE, null=True, blank=True)
    server_name = CharField(max_length=30, null=False, unique=True)
    server_ip = CharField(max_length=14, null=True, blank=True)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=True, blank=True)
    ram_gb = DecimalField(decimal_places=1, max_digits=3, null=True, blank=True)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    datacenter = ForeignKey(Datacenter, on_delete=deletion.CASCADE, null=True, blank=True)
    node_role = CharField(choices=NodeRoleChoices.choices, max_length=20, null=False, default='')
    server_health = CharField(choices=ServerHealthChoices.choices, max_length=20, null=True, blank=True)
    last_reboot = DateTimeField(null=True, blank=True)
    dbms_type = CharField(choices=DbmsTypeChoices.choices, max_length=20, null=True, blank=True)
    os_version = CharField(max_length=30, null=True, blank=True)
    os_patched_dttm = DateTimeField(null=True, blank=True)
    db_version = CharField(max_length=30, null=True, blank=True)
    db_version_number = IntegerField(validators=[MinValueValidator(0)], null=True, blank=True)
    db_patched_dttm = DateTimeField(null=True, blank=True)
    pending_restart_sw = BooleanField(null=False, default=False)
    metrics_sw = BooleanField(null=False, default=True)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class ApplicationContact(Model):
    class Meta:
        db_table = "dbaas_application_contact"

    application = ForeignKey(Application, on_delete=deletion.CASCADE, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.CASCADE, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    updated_dttm = DateTimeField(auto_now=True, null=False)


class Backup (models.Model):
    class Meta:
        db_table = "dbaas_backup"
        ordering = ['start_dttm']

    class BackupTypeChoices(DjangoChoices):
        BACKUPFULL = ChoiceItem("Full", "Full", 1)
        BACKUPINCREMENTAL = ChoiceItem("Incr", "Incremental", 2)
        BACKUPDIFFERENTIAL = ChoiceItem("Diff", "Differential", 3)

    class BackupStatusChoices(DjangoChoices):
        RUNNING = ChoiceItem("Running", "Running", 1)
        FAILED = ChoiceItem("Failed", 'Failed', 2)
        SUCCESSFUL = ChoiceItem("Successful", "Successful", 3)

    cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False)
    backup_type = CharField(max_length=10, null=False, choices=BackupTypeChoices.choices, default=BackupTypeChoices.BACKUPFULL)
    backup_status = CharField(max_length=15, choices=BackupStatusChoices.choices, null=True, blank=True)
    db_size_gb = DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    backup_size_gb = DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    stop_dttm = DateTimeField(null=True, blank=True)
    deleted_dttm = DateTimeField(null=True, blank=True)
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
        db_table="dbaas_restore"

    class RestoreTypeChoices(DjangoChoices):
        RESTOREFULL = ChoiceItem("Full", "Restore Full", 1)
        RESTOREDB = ChoiceItem("DB", "Restore Database", 2)
        RESTORETABLE = ChoiceItem("Table", "Restore Table", 3)

    class RestoreStatusChoices(DjangoChoices):
        RUNNING = ChoiceItem("Running", "Running", 1)
        FAILED = ChoiceItem("Failed", 'Failed', 2)
        SUCCESSFUL = ChoiceItem("Successful", "Successful", 3)

    from_cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False, related_name='restore_from_cluster')
    to_cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False, related_name='restore_to_cluster')
    restore_type = CharField(max_length=10, null=False, choices=RestoreTypeChoices.choices, default='')
    restore_to_dttm = DateTimeField(editable=False)
    restore_status = CharField(max_length=15, choices=RestoreStatusChoices.choices, null=True, blank=True)
    restore_by = CharField(max_length=30, null=False, default='')
    ticket = CharField(max_length=30, null=True, blank=True)
    start_dttm = DateTimeField(editable=False, auto_now_add=True, null=False)
    stop_dttm = DateTimeField(null=True, blank=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def duration(self):
        return self.stop_dttm-self.start_dttm

class ServerActivity(models.Model):
    class Meta:
        db_table = "dbaas_server_activities"
        ordering = ['created_dttm']

    class ActivitiesStatusChoices(DjangoChoices):
        QUEUED = ChoiceItem("Queued", "Queued", 1)
        PENDINGRESTART = ChoiceItem("PendingRestart", 'PendingRestart', 2)
        PROCESSING = ChoiceItem("Processing", "Processing", 3)
        SUCCESSFUL = ChoiceItem("Successful", "Successful", 4)
        FAILED = ChoiceItem("Failed", "Failed", 5)

    class ActivityTypeChoices(DjangoChoices):
        RESTARTSERVER = ChoiceItem("RestartServer", "Restart Server", 1)
        STOPSERVER = ChoiceItem("StopServer", "Stop Server", 2)
        STARTSERVER = ChoiceItem("StartServer", "Start Server", 3)
        RESTARTDB = ChoiceItem("RestartDB", "Restart Database", 4)
        PROMOTEDB = ChoiceItem("PromoteDB", "Promote Database", 5)
        DEMOMOTEDB = ChoiceItem("DemoteDB", "Demote Database", 6)
        CREATEDB = ChoiceItem("CreateDB", "Create Database", 7)
        DISTROYEDDB = ChoiceItem("DISTROYDB", "Destroy Database", 8)

    server = ForeignKey(Server, on_delete=deletion.CASCADE, null=False)
    activity_type = CharField(max_length=20, null=False, choices=ActivityTypeChoices.choices, default=ActivityTypeChoices.CREATEDB)
    start_dttm = DateTimeField(null=True, blank=True)
    stop_dttm = DateTimeField(null=True, blank=True)
    activity_status = CharField(max_length=20, null=False, choices=ActivitiesStatusChoices.choices, default=ActivitiesStatusChoices.QUEUED)
    activity_by = CharField(max_length=30, null=False, default='')
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class ClusterNote(models.Model):
    class Meta:
        db_table = "dbaas_cluster_note"
        ordering = ['created_dttm']

    cluster = ForeignKey(Cluster, on_delete=deletion.CASCADE, null=False)
    title = CharField(max_length=50)
    note = CharField(max_length=2048, null=True, blank=True)
    ticket = CharField(max_length=30, null=True, blank=True)
    created_by = CharField(max_length=30, null=False, default='')
    note_color = CharField(max_length=15, null=True, blank=True, choices=ColorChoices.choices)
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
