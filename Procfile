web: gunicorn project_django.wsgi --log-file - 
#or works good with external database
web: python manage.py migrate && gunicorn project_django.wsgi
