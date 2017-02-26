from django.core.management import setup_environ

from hksearcher import settings
from hksearcher.web.models import Motor

setup_environ(settings)

motors = Motor.objects.all()
for i in motors:
    print(i)
    i.delete()