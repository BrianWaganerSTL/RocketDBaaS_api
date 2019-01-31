from django.test import TestCase
from rest_framework import status

from dbaas.models import Cluster, Application


class Test_Application(TestCase):
  def test_create_application(self):
    data = {"application_name":"TestThisB","active_sw":True}
    response = self.client.post('/dbaas_api/applications/', data, format='json')
    self.assertEquals(response.status_code, status.HTTP_201_CREATED)
    self.assertEquals(Application.objects.count(), 1)
    self.assertEquals(Application.objects.get().application_name,'TestThisB')

class Test_AppClusterServers(TestCase):
  def test_app_cluster_servers(self):
    data = {"application_name":"TestThisB","environment_name":"Sbx","dbms_type":"PostgreSQL","cluster_name":"TestCluster","tls_enabled_sw":True,"backup_retention_days":14,"servers_ids":[1,2]}
    data = {"application_name":"TestThisB","environment_name":"Sbx","dbms_type":"PostgreSQL","cluster_name":"TestCluster","tls_enabled_sw":True,"backup_retention_days":14}

    response = self.client.post('/dbaas_api/clusters/', data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(Cluster.objects.count(), 1)
    self.assertEqual(Cluster.objects.get().cluster_name, 'TestCluster')
