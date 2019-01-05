<h1>Setup of the Project</h1>

Don't forget to add the local_settings.py file right next to the settings.py file.

<h3>Installs</h3>

 * venv
 * pip3 install django
 * django-admin startproject
 * python3 manage.py runserver

<h3>Install via PyCharm</h3>
```
CTRL+ALT+s
```

* Add Django
  * Set Settings to the settings.py in the RocketDBaaS_api/RocketDBaaS directory

* Add venv

<h3>Create a Application User so you can login</h3>
```
manage.py@RocketDBaaS > createsuperuser
Username:  RocketDBaaS
Email address:
Password:  RocketDBaaS
```

<h3>Dump the current database if you want that to be test data for later</h3>
manage.py 
```
dumpdata --indent 2 -o dbaas/fixtures/test_data.json dbaas
dumpdata --indent 2 -o monitor/fixtures/test_data.json monitor
```

<h2>Clear just the data in the tables</h2>
<h4>Clear the tables data</h4>

This whips out your data for the application and your web users and roles.  Users and Roles are not part of the load data.
```
flush
```

<h4>Import your test data</h4>
```
loaddata --app dbaas dbaas/fixtures/test_data.json
loaddata --app monitor monitor/fixtures/test_data.json
```

<h4>Create a Application User so you can login</h4>
```
manage.py@RocketDBaaS > createsuperuser
Username:  RocketDBaaS
Email address:
Password:  RocketDBaaS
```

<h2>If you need to drop the tables and start over</h2>

<h4>Run the following to show you what table to drop</h4>

```

- drop all your views and tables in the schema that you have models for via pgAdmin
makemigrations
- copy the fixtures/CreateViews.py to /migrations/0002_CreateViews
migrate --fake-initial
migrate
loaddata --app dbaas dbaas/fixtures/test_data.json
loaddata --app monitor monitor/fixtures/test_data.json
```

<h3>If you add more pip packages save your new Requirements</h3>
```angular2html
pip freeze > requirements.txt
```

<h3><i>LoadData not all That!</i></h3>
I have tried loaddata, but it does an insert for every row.  Sometimes a SQL statement is just better.

When I tried loaddata to load the server_port table it would have taken over 1 hour, with the API on my laptop and the database being on a Redhat Server.  Probably a firewall issues.

```sql92
CREATE database "RocketDB" WITH OWNER = postgres ENCODING = 'UTF8' CONNECTION LIMIT = -1;

!python manage.py makemigrations

!python manage.py migrate

!python manage.py createsuperuser
   Username: RocketDBaaS
   Email Address:
   Password: RocketDBaaS
   
insert into dbaas_servers_port
  select port, 'Free', '', now()
  from generate_series(1024,65535) as port;
  
update dbaas_servers_port
  set port_status = 'Hidden', port_note = 'Reserved for other processes'
where port in (4200,8000,2379,2380);

insert into dbaas_environment values 
  ('Sbx',1),('Dev',2),('QA',3),('UAT',4),('Prod',5);
  
insert into dbaasdatacenter values 
  (1, 'CH', 1), (2, 'PA', 2);
 

```