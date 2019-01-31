# from django.test import TestCase
#
# from dbaas.models import Server
#
#
# class PoolServersTestCases(TestCase):
#  def setUp(self):
#    self.poolServer = Server();
#    self.poolServer.environment = 'Sbx'
#    self.poolServer.dbms_type = 'PostgreSQL'
#    self.poolServer.server_name = 'TestTestTestTest'
#    self.poolServer.cpu = 4
#    self.poolServer.ram_gb = 4
#    self.poolServer.db_gb = 10
#    self.poolServer.node_role = Server.NodeRoleChoices.POOLSERVER
#    self.poolServer.active_sw = True
#
# #   # def test_create_pool_server(self):
# #   #   response = self.client.post('/dbaas_api/poolservers/', self.poolServer)
# #   #   # self.assertEquals(response.status_code, 201)
