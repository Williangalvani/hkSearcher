import os, sys
path = '/root/hksite/'
if path not in sys.path:
   sys.path.append(path)

os.environ["DJANGO_SETTINGS_MODULE"] = "hksearcher.settings"
from web.models import Battery
import settings
from django.core.management import setup_environ
import re
setup_environ(settings)

motors = Battery.objects.all()
for i in motors:
    print i
    i.delete()
