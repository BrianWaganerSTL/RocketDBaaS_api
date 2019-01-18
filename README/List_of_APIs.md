<h1>RocketDBaaS APIs</h1>

<h3>Swagger Documents</h3>

http://localhost:8000/docs/


<h3>General</h3>

http://localhost:8000/dbaas_api/applications/

http://localhost:8000/dbaas_api/poolservers/

http://localhost:8000/dbaas_api/poolservers/:id/

http://localhost:8000/dbaas_api/poolservers/?dbms=PostgreSQL&env=SBX&req_cpu=2&req_ram_gb=8&req_ram_gb=8&status_in_pool=Available

http://localhost:8000/dbaas_api/clusters/

http://localhost:8000/dbaas_api/clusters/:id/

http://localhost:8000/dbaas_api/environments/

http://localhost:8000/dbaas_api/environments/:id/

http://localhost:8000/dbaas_api/dbmstypes/


<h3>Cluster Details Tabs</h3>

http://localhost:8000/dbaas_api/applications/:vApplicationId/contacts/

http://localhost:8000/dbaas_api/clusters/:vClusterId/servers/

http://localhost:8000/dbaas_api/clusters/:vClusterId/backups/

http://localhost:8000/dbaas_api/clusters/:vClusterId/restores/

http://localhost:8000/dbaas_api/clusters/:vClusterId/notes/

http://localhost:8000/dbaas_api/servers/:vServerId/activities/

http://localhost:8000/dbaas_api/servers/:vServerId/incidents/


<h3>Metrics</h3>

http://localhost:8000/dbaas_api/servers/:vServerId/metrics/cpu/

http://localhost:8000/dbaas_api/servers/:vServerId/metrics/load/

http://localhost:8000/dbaas_api/servers/:vServerId/metrics/mountpoints/

http://localhost:8000/dbaas_api/servers/:vServerId/metrics/pingserver/

http://localhost:8000/dbaas_api/servers/:vServerId/metrics/pingdb/


<h3>Charts</h3>

http://localhost:8000/dbaas_api/servers/:vServerId/charts/mountpoints/
