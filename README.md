# Statusflex

Statusflex is status page software to inform users about incients with services.
This software is in alpha development stage. You can use it on production at your risk.

### Usage

Go to /admin page, select Watchdog -> Services and fill name of service and it's check url.
Now Statusflex will take care of service and inform about failures
and give some statistics about service. If you want to inform users about maintenances or informations about failure
you can write them by Journal -> Reports.

### Installation

There is no installer included.
You need to run this command to migrate database and install dependencies.

```
pip install -r requirements.txt && python manage.py migrate
```

You need to create admin:
``` 
python manage.py createsuperuser
```

And run it by:
```
python manage.py runserver
```


### Cron

This software works well when it's updated every minute, but it doesn't have background cron tasks now cause of limitations of language 
and framework. It will support this soon, but now your can setup cron task:

```
*/1 * * * * curl http://localhost/
```