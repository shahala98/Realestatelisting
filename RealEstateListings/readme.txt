Username (leave blank to use 'hp'): capstoneproject
Email address: fthma@gmail.com
Password:fthma@98


installed django
Django framework installed


python manage.py startproject review_project # renamed project
startapp app names
python -m venv celeryenv # not mandotery for celery
celeryenv/Scripts/activate
pip install django
pip install pillow # photo upload cheyan
pip install celery 

1. settings.py
add app name
urls.py
and add = EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = '' # email>security>app password>app name>password
EMAIL_HOST_PASSWORD = '' # my email
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = '' # my emal

project folder create celery.py

2. app
models.py
create urls
forms.py
views.py
email.py

templates
create template and
email_meaasge.txt # write email message

celery -A CeleryReview  worker --pool=solo -l info


https://themewagon.com/themes/free-bootstrap-5-real-estate-website-template-property/
