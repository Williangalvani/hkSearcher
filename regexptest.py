from django.core.management import setup_environ

from hksearcher import settings
from web.models import Motor

setup_environ(settings)

import re
    

motors = Motor.objects.all()



 
def extractThrust(source):
        thrust =  re.compile(r'(?:Thrust|Pulls?)\s*:?\s*[^ ^0-9]{0,10}\s*(?:(?:\d+.\d+|\d+).?\s*)+(?:k?gr?a?m?s?|oz)',re.IGNORECASE)
        thrust2 = re.compile(r'(?:\d+[/.,]\d+|\d+)+(?:k?gr?a?m?s?|oz)\s?.{0,2}\sthrust',re.IGNORECASE)
        
        found = []
        for regexp in [thrust,thrust2]:
            found.append(re.findall(regexp, source))
        numbers = []
        
        for i in found:
            for i2 in i:
                if "my" not in i2 and " a " not in i2:
                    s = str(i2).lower()
                    factor = 1
                    print i2
                    if "kg" in s:
                        factor = 1000
                    elif "oz"in s:
                        factor = 28.34
                    else:
                        factor = 1
                    strings = [s]
                    if ", " in s:
                        strings = s.split(", ")
                    for string in strings:
                        all = re.findall(r"[-+]?\d*\.\d+|\d+",string)
                        for number in all:
                            if number.replace('.','').isdigit():
                                print float(number) , s
                                numbers.append(float(number)*factor)
                if numbers:
                    #print max(numbers)
                  
                    #print self.maxThrust
                    return max(numbers)
        return None
        
        
        
        
print dir(Motor)
print Motor._meta.db_tablespace
print dir(Motor.__metaclass__.__base__)
        
        
        
        
        
        
        
        
        
        
        
        
 