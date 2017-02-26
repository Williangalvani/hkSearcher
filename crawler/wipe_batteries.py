from hksearcher.web.models import Battery
from hksearcher import settings
from django.core.management import setup_environ
import re
setup_environ(settings)

motors = Battery.objects.all()
for i in motors:
    print i
    i.delete()