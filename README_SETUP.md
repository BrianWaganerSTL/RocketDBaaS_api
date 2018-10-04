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
  * Set Settings to the settings.py in the RocketDBaaS/RocketDBaaS directory

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
  dumpdata --indent 2 -o dbaas/fixtures/test_data.json --exclude dbaas.ApplicationContactsDetailsView dbaas
```

<h3>Clear the tables data</h3>

This whips out your data for the application and your web users and roles.  Users and Roles are not part of the load data.
```
flush
```

<h3>Import your test data</h3>
```
    loaddata --app dbaas dbaas/fixtures/test_data.json
```

<h3>Create a Application User so you can login</h3>
```
manage.py@RocketDBaaS > createsuperuser
Username:  RocketDBaaS
Email address:
Password:  RocketDBaaS
```