# class Test_AppClusterServers(TestCase):
#   def setUp(self):
#     self.poolServer = ;
#     self.poolServer.environment = 'Sbx'
#     self.poolServer.dbms_type = 'PostgreSQL'
#     self.poolServer.server_name = 'TestTestTestTest'
#     self.poolServer.cpu = 4
#     self.poolServer.ram_gb = 4
#     self.poolServer.db_gb = 10
#     self.poolServer.node_role = Server.NodeRoleChoices.POOLSERVER
#     self.poolServer.active_sw = True
#
#   def test_app_cluster_servers(self):
#     response = self.client.post(
#       '/dbaas_api/cluster/',
#       'application_name:TestThisB
#     environment_name: Sbx
#     dbms_type: PostgreSQL
#     cluster_name: TestClust
#     tls_enabled_sw: true
#     backup_retention_days: 14
#     servers_ids: [1, 2]
#                                 )
#     # self.assertEquals(response.status_code, 201)
