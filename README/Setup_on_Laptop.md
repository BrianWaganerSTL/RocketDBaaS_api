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

drop database "RocketDBaaS";
create database "RocketDBaaS";
makemigrations
migrate
# The load takes about 1 minute
loaddata --app dbaas dbaas/fixtures/test_data.json   
```
```angular2html
createsuperuser
    Username:  RocketDBaaS
    Email address:
    Password:  RocketDBaaS
```

<h3>If you add more pip packages save your new Requirements</h3>
```bash
pip freeze > requirements.txt
```

<h3>To get around the issue of not being able to do pip internet installs on servers/h3>
```bash
pip wheel --wheel-dir=../wheels -r requirements.txt
```