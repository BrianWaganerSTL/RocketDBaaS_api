from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Model, CharField, DecimalField, BooleanField, DateTimeField, IntegerField, EmailField, ForeignKey, deletion
from django.utils import timezone
from djchoices import DjangoChoices, ChoiceItem

class DbmsTypeChoices(DjangoChoices):
    NULL = ChoiceItem("")
    PostgreSQL = ChoiceItem()
    MongoDB = ChoiceItem()


class PoolServer(Model):
    class StatusInPoolChoices(DjangoChoices):
        NULL = ChoiceItem("")
        Available = ChoiceItem("Available")
        Locked = ChoiceItem("Locked for Build")
        Used = ChoiceItem("Used")

    serverName = CharField(max_length=30, null=False)
    serverIp = CharField(max_length=14, null=False)
    dbmsType = CharField(max_length=10, null=False, choices=DbmsTypeChoices.choices)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    memGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
    dbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
    dataCenter = CharField(max_length=20, null=False)
    statusInPool = CharField(max_length=10, null=False, choices=StatusInPoolChoices.choices)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)


class Environment(Model):
    envName = CharField(max_length=5, null=False)
    envFullName = CharField(max_length=25, null=False)
    activeSw = BooleanField(null=False)

    def __str__(self):
        return self.envName


class Contact(Model):
    contactName = CharField(max_length=60, null=False)
    contactType = CharField(max_length=30)
    contactEmail = EmailField
    contactPhone = CharField(max_length=15)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.contactName


class Application(Model):
    appName = CharField(max_length=40, null=False)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.appName


class Cluster(Model):
    clusterName = CharField(max_length=30, null=False)
    dbmsType = CharField(choices=DbmsTypeChoices.choices, max_length=10, null=False)
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    environment = ForeignKey(Environment, on_delete=deletion.ProtectedError, null=False)
    requestedCpu = IntegerField(validators=[MinValueValidator(2),MaxValueValidator(14)], null=False)
    requestedMemGigs = IntegerField(validators=[MinValueValidator(2),MaxValueValidator(64)], null=False)
    requestedDbGigs = IntegerField(validators=[MinValueValidator(0),MaxValueValidator(102400)], null=False)
    haPort = IntegerField(validators=[MinValueValidator(1024),MaxValueValidator(65535)])
    tlsEnabled = BooleanField(null=False)
    backupRetentionDays = IntegerField(validators=[MinValueValidator(1),MaxValueValidator(30)], null=False)
    health = CharField(max_length=20, null=False)
    activeSw = BooleanField(null=False)
    effDttm = DateTimeField(default=timezone.now)
    expDttm = DateTimeField
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.clusterName


class Server(Model):
    cluster = ForeignKey(Cluster, on_delete=deletion.ProtectedError, null=False)
    serverName = CharField(max_length=30, null=False)
    serverIp = CharField(max_length=14, null=False)
    cpu = DecimalField(decimal_places=1, max_digits=3, null=False)
    memGigs = DecimalField(decimal_places=1, max_digits=3, null=False)
    dbGigs = DecimalField(decimal_places=2, max_digits=4, null=False)
    dataCenter = CharField(max_length=20, null=False)
    arbiterNodeSw = BooleanField(null=False)
    osVersion = CharField(max_length=30)
    dbVersion = CharField(max_length=30)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.serverName




class ApplicationContact(Model):
    application = ForeignKey(Application, on_delete=deletion.ProtectedError, null=False)
    contact = ForeignKey(Contact, on_delete=deletion.ProtectedError, null=False)
    activeSw = BooleanField(null=False)
    createdDttm = DateTimeField(editable=False, auto_now_add=True)
    updatedDttm = DateTimeField(auto_now=True)

    def __str__(self):
        return self.application.appName + ': ' + self.contact.contactName