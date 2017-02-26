'''
Created on Nov 9, 2011

@author: will
'''

# -*- coding: UTF-8 -*-    

from crawler.motor import Motor

from crawler.urlfetcher import parseUrl
from web.models import Motor
from hksearcher import settings
from django.core.management import setup_environ
import re
setup_environ(settings)

motors = Motor.objects.all()
thrust =  re.compile(r'(?:Thrust|Pulls?)\s*:?\s*[^ ^0-9]{0,10}\s*(?:(?:\d+.\d+|\d+).?\s*)+(?:k?gr?a?m?s?|oz)',re.IGNORECASE)

print re.findall(thrust,'11V 10.5A*2 Thrust:1320g/46.56oz')