from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem


class EnvironmentChoices(DjangoChoices):
    SBX = ChoiceItem("SBX","Sandbox",1)
    DEV = ChoiceItem("DEV","Development",2)
    QA = ChoiceItem("QA","Quality Assurance",3)
    UAT = ChoiceItem("UAT","User Acceptance Testing",4)
    PRD = ChoiceItem("PRD","Production",5)
    PPD = ChoiceItem("PPD","Post Production",6)


class DbmsTypeChoices(DjangoChoices):
    PostgreSQL = ChoiceItem()
    MongoDB = ChoiceItem()


class PoolServer(Model):
    class Meta:
        db_table = "pool_server"

    class StatusInPoolChoices(DjangoChoices):
        Available = ChoiceItem("Available","Available",1)
        Locked = ChoiceItem("Locked","Locked for Build",2)
        Used = ChoiceItem("Used","Used",3)

    environment = CharField(choices=EnvironmentChoices.choices, max_length=20, null=False, blank=True)
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    dbms_type = CharField(max_length=10, null=False, blank=True, choices=DbmsTypeChoices.choices)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    mem_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = CharField(max_length=20, null=False)
    status_in_pool = CharField(max_length=20, null=False, blank=True, choices=StatusInPoolChoices.choices)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)


class Contact(Model):
    class Meta:
        db_table = "contact"

    class ContactTypeChoices(DjangoChoices):
        Person = ChoiceItem("Person","Person",1)
        Group = ChoiceItem("Distro","Email Group Distro",2)
        API = ChoiceItem("API","API Endpoint",3)

    contact_name = CharField(max_length=60, null=False)
    contact_type = CharField(max_length=30, choices=ContactTypeChoices.choices, null=True)
    contact_email = EmailField
    contact_phone = CharField(max_length=15)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contact_name


class Application(Model):
    class Meta:
        db_table = "application"

    application_name = CharField(max_length=40, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.application_name


class Cluster(Model):
    class Meta:
        db_table = "cluster"

    cluster_name = CharField(max_length=30, null=False)
    dbms_type = CharField(choices=DbmsTypeChoices.choices, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    environment = CharField(choices=EnvironmentChoices.choices, max_length=20, null=False, blank=True)
    requested_cpu = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(14)], null=False)
    requested_mem_gb = IntegerField(validators=[MinValueValidator(2), MaxValueValidator(64)], null=False)
    requested_db_gb = IntegerField(validators=[MinValueValidator(0), MaxValueValidator(102400)], null=False)
    haproxy_port = IntegerField(validators=[MinValueValidator(1024), MaxValueValidator(65535)])
    tls_enabled_sw = BooleanField(null=False)
    backup_retention_days = IntegerField(validators=[MinValueValidator(1), MaxValueValidator(30)], null=False)
    health = CharField(max_length=20, null=False)
    active_sw = BooleanField(null=False, default=True)
    eff_dttm = DateTimeField(default=timezone.now)
    exp_dttm = DateTimeField
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.cluster_name


class Server(Model):
    class Meta:
        db_table="server"
    class NodeRoleChoices(DjangoChoices):
        Primary = ChoiceItem("Primary","Primary Node",1)
        SecondarySync = ChoiceItem("SecondarySync","Secondary Node - Replication is Synchronous",2)
        SecondaryAsync = ChoiceItem("SecondaryAsync","Secondary Node- Replication is Asynchronous",3)
        Arbiter = ChoiceItem("Arbiter","Arbiter Node",4)


    cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False)
    server_name = CharField(max_length=30, null=False)
    server_ip = CharField(max_length=14, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    mem_gb = DecimalField(decimal_places=1, max_digits=3, null=False)
    db_gb = DecimalField(decimal_places=2, max_digits=5, null=False)
    data_center = CharField(max_length=20, null=False)
    node_role = CharField(choices=NodeRoleChoices.choices, max_length=20, null=False, blank=True)
    os_version = CharField(max_length=30)
    db_version = CharField(max_length=30)
    pending_restart_sw = BooleanField(null=False, default=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.server_name


class ApplicationContact(Model):
    class Meta:
        db_table="application_contact"

    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.ProtectedError, null=False)
    active_sw = BooleanField(null=False, default=True)
    created_dttm = DateTimeField(editable=False, auto_now_add=True)
    updated_dttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.application.application_name + ': ' + self.contact.contact_name