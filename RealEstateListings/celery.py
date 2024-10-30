from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RealEstateListings.settings')
app = Celery('RealEstateListings')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))














