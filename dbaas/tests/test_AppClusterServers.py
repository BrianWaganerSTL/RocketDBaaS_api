from django.test import TestCase
from rest_framework import status

from dbaas.models import Cluster, Application, ServerPort, Server, Environment, Datacenter


class Test_Application(TestCase):
  def test_create_application(self):
    data = {"application_name":"TestThisB","active_sw":True}
    response = self.client.post('/dbaas_api/applications/', data, format='json')
    self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    self.assertEquals(Application.objects.count(), 1)
    self.assertEquals(Application.objects.get().application_name,'TestThisB')


class Test_Environment(TestCase):
  def test_create_application(self):
    Environment(env_name='Sbx').save()
    self.assertEquals(Environment.objects.count(), 1)
    self.assertEquals(Environment.objects.get().env_name,'Sbx')


class Test_Datacenter(TestCase):
  def test_create_application(self):
    Datacenter(datacenter='CH').save()
    self.assertEquals(Datacenter.objects.count(), 1)
    self.assertEquals(Datacenter.objects.get().datacenter,'CH')


class Test_ServerPorts(TestCase):
  def test_open_ports(self):
    self.assertEquals(ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.FREE).count(), 0)

  def test_adding_open_serverports(self):
    ServerPort(port=10000, port_status=ServerPort.PortStatusChoices.FREE, port_notes='Free Tests').save()
    self.assertEquals(ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.FREE).count(), 1)


class Test_Servers(TestCase):
  def test_create_server(self):
    Server(server_name='WreckItRyan', node_role=Server.NodeRoleChoices.CONFIGURING).save()
    self.assertEquals(Server.objects.count(), 1)
    self.assertEquals(Server.objects.get().server_name, 'WreckItRyan')

    Server(server_name='CheckItOrWreckIt', node_role=Server.NodeRoleChoices.PRIMARY).save()
    self.assertEquals(Server.objects.count(), 2)
    self.assertEquals(Server.objects.filter(server_name='CheckItOrWreckIt').count(), 1)


class Test_AppClusterServers(TestCase):
  def test_app_cluster_servers(self):
    env = Environment(env_name='Sbx').save()

    Server(server_name='WreckItRyan', node_role=Server.NodeRoleChoices.CONFIGURING).save()
    Server(server_name='CheckItOrWreckIt', node_role=Server.NodeRoleChoices.PRIMARY).save()
    s1 = Server.objects.filter(server_name='WreckItRyan').first()
    s2 = Server.objects.filter(server_name='CheckItOrWreckIt').first()

    ServerPort(port=10000, port_status=ServerPort.PortStatusChoices.FREE, port_notes='Free Tests').save()
    ServerPort(port=10001, port_status=ServerPort.PortStatusChoices.FREE, port_notes='Free Tests').save()
    self.assertEquals(ServerPort.objects.filter(port_status=ServerPort.PortStatusChoices.FREE).count(), 2)

    data = {"application_name":"TestThisB","environment_name":"Sbx","dbms_type":"PostgreSQL","cluster_name":"TestCluster","tls_enabled_sw":True,"backup_retention_days":14}
    serverIds = []
    serverIds.append(s1.id)
    serverIds.append(s2.id)
    data['server_ids'] = serverIds
    print(data)

    response = self.client.post('/dbaas_api/clusters/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Cluster.objects.count(), 1)
    self.assertEqual(Cluster.objects.get().cluster_name, 'TestCluster')
