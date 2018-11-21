from django.test import TestCase


class SimpleTest(TestCase):
    def test_MyPoolServers_Post_HappyPath(self):
        response = self.client.post('/api/MyPoolServers/',
                    {
                        "server_name": "abc9_PostMan",
                        "server_ip": "9",
                        "dbms_type": "PostgreSQL",
                        "cpu": "2.0",
                        "ram_gb": "2.0",
                        "db_gb": "10.00",
                        "data_center": "DC",
                        "status_in_pool": "Available"
                    })
        self.assertEquals(response.status_code, 201)
