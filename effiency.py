
from crawler.motor import Motor

from crawler.urlfetcher import parseUrl
from web.models import Motor
from hksearcher import settings
from django.core.management import setup_environ
import re
#setup_environ(settings)

motors = Motor.objects.all().order_by('kv')
effience = []
for motor in motors:
    if motor.getEff():
        print motor.getEff(), motor.name
