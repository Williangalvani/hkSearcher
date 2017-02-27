from django.core.management import setup_environ

from hksearcher import settings
from hksearcher.web.models import Battery

setup_environ(settings)

motors = Battery.objects.all()
for i in motors:
    print
    i
    i.delete()
