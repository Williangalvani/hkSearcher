'''
Created on Feb 24, 2012

@author: Will
'''
from urlfetcher import parseUrl
from hksearcher.web.models import Motor as Motordb
import re
import string

from hksearcher.crawler import urlfetcher


root = 'http://www.hobbyking.com/hobbyking/store/'


class Motor(object):
    kv = None
    name = None
    price = None
    rating = None
    img = None
    bigimg = None
    page = None
    weight = None
    maxCurrent = None
    resistance = None
    power = None
    maxVoltage = None
    description = None
    reviews = None
    id = None
    thrusts = []
    nthrusts = []
    
    def getReviews(self):
        if not self.reviews:
            self.reviews = parseUrl('reviewsSubframe.asp?idproduct=' + self.id + "&more=1")
        return self.reviews
    
    def extractThrust(self,source):
        thrust =  re.compile(r'(?:Thrust|Pulls?|Pulled)\s*:?\s*[^ ^0-9]{0,10}\s*(?:(?:\d+[/.,]\d+|\d+).?\s*)+(?:k?gr?a?m?s?|ozs?|lbs?)',re.IGNORECASE)
        thrust2 = re.compile(r'(?:\d+[/.,]\d+|\d+)+(?:k?gr?a?m?s?|ozs?|lbs?)\s?.{0,2}\sthrust',re.IGNORECASE)
        
        found = []
        for regexp in [thrust,thrust2]:
            found.append(re.findall(regexp, source))
        numbers = []
        
        for i in found:
            for i2 in i:
                if "my" not in i2 and " a " not in i2:
                    s = str(i2).lower()
                    factor = 1
                    print i
                    if "kg" in s:
                        factor = 1000
                    if "oz"in s:
                        factor = 28.34
                    if "lb"in s:
                        factor = 453.6
                    strings = [s]
                    if ", " in s:
                        strings = s.split(", ")
                    for string in strings:
                        all = re.findall(r"[-+]?\d*[\.,]\d+|\d+",string)
                        for number in all:
                            if number.replace('.','').isdigit():
                                numbers.append(float(number)*factor)
            if numbers:
                #print max(numbers)
                self.maxThrust = max(numbers)
                #print self.maxThrust
                return self.maxThrust
        return None
        
    def getThrust(self):
        self.extractThrust(self.description)
        if not self.maxThrust:
            
            print "trying reviews!"
            self.getReviews()
            self.extractThrust(str(self.reviews))
            if not self.maxThrust:
                thrust =  re.compile(r'(?:(Thrust|Pulls?))+(:?\s*.{0,10}\s*\d+k?g+)',re.IGNORECASE)
                thrust2 = re.compile(r'(?:(Thrust|Pulls?))(:?\s*.{1,10}\s*\d+oz)',re.IGNORECASE)
                thrust3 = re.compile(r'(?:(thrust|Pulls?))(.\s*\d+k?g)',re.IGNORECASE)
                thrust4 = re.compile(r'(?:(thrust|Pulls?))(.\s*\d+oz)',re.IGNORECASE)
                
                thrust5 = re.compile(r'(?:(thrust|Pulls?))(:?\s*.{1,10}\s*\dk?g)',re.IGNORECASE)
                thrust6 = re.compile(r'(?:(thrust|Pulls?))(:?\s*.{1,10}\s*\doz)',re.IGNORECASE)
                thrust7 = re.compile(r'(?:\d+|\d+.\d+)gr?a?m?m?s?\s?.{0,2}\sthrust',re.IGNORECASE)
                thrust8 = re.compile(r'(?:\d+|\d+.\d+)ozs?.{0,2}\sthrust',re.IGNORECASE)
                for regexp in [thrust,thrust2,thrust3,thrust4,thrust5,thrust6,thrust7,thrust8]:
                    found = re.findall(regexp, str(self.reviews).rstrip('\n'))
                    if found:
                        for thrust in found:
                            self.thrusts.append(str(thrust))
                #print self.thrusts
                for thrust in self.thrusts:
                    all=string.maketrans('','')
                    nodigs=all.translate(all, string.digits)
                    
                    if 'oz' in thrust.lower() and not "my"  in thrust:
                        self.nthrusts.append(float(re.findall(r"[-+]?\d*\.\d+|\d+",thrust)[0])*28.34)
                    elif 'kg' in thrust.lower() and not "my"  in thrust:
                        self.nthrusts.append(float(re.findall(r"[-+]?\d*\.\d+|\d+",thrust)[0])*1000)
                    elif not "my"  in thrust:
                        
                        self.nthrusts.append(float(re.findall(r"[-+]?\d*\.\d+|\d+",thrust)[0])*1)
                if self.nthrusts:
                    self.maxThrust = max(self.nthrusts)        
                else:
                    self.maxThrust = None
                
                if self.reviews and 'thrust' in self.reviews:
                    print self.reviews
                    
            
    def addToDb(self):
  
            dbmotor = Motordb()
            dbmotor.name = self.name
            dbmotor.kv = self.kv
            dbmotor.price = self.price
            dbmotor.rating = self.rating
            dbmotor.img = self.img
            dbmotor.page = self.page
            dbmotor.weight = self.weight
            dbmotor.maxCurrent = self.maxCurrent
            dbmotor.maxVoltage = self.maxVoltage
            dbmotor.resistance = self.resistance
            dbmotor.power = self.power
            dbmotor.bigimg =self.bigimg
            dbmotor.description = self.origdescription
            dbmotor.maxThrust = self.maxThrust
            dbmotor.save()
            
    
    def __str__(self):
        return "\n\n" + str(self.name)         + "  \npage = "+ str(self.page) + "  \nkv = " + str(self.kv) + " \nrating = " + str(self.rating) + " \nprice = " + str(self.price) + " \nPower = " + str(self.power) + " \nweight = " + str(self.weight) 

    def getKv(self):
        kv = None
        if "kv" in self.name.lower():
            string = self.name.lower().split('kv')[0]
            if string.rfind(" ") < string.rfind('-'):
                kv = string.split("-").pop()
            else:
                kv = string.split(" ").pop()
            while(len(kv)>1 and not kv.replace(".","").isdigit()):
                kv = kv[1:]
            return kv
        return None
    
    def getRating(self,i):
        ratingstring = i.find('td' ,background="images/new07/bgd05.jpg").img['src']
        return ratingstring.split("/").pop()[0:1]
    
    def extract(self,unit):
        string = self.description.lower().split(unit)[0]
        string = string.replace(" ","")
        string = string.split("a").pop()
        while(not string.replace(".","").isdigit() and len(string)>0):
            string = string[1:]
        if len(string)>0:
            return string
        return None
        
        
    def extractKv(self):
        brushed = re.compile(r'\s?\d+V/\d+.\d+rpm',re.IGNORECASE)
        found = re.findall(brushed, self.origdescription)
        if found:
            number = found.pop().split("rpm")[0].split("/").pop()
            number = re.findall(r"[-+]?\d*\.\d+|\d+",number)[0]
            while not number.isdigit() and len(number)>0:
                number = number[1:]
            if number:
                if self.maxVoltage:
                    return int(float(number) / float(self.maxVoltage))

    def extractWeight(self):
        trys = ["grams","gram","g)","g "]
        text = self.name.lower() + " " + self.description.lower()
        found = None
        for i in trys:
            if i in text:
                found = i
        if found:
            for i in text.lower().split(found):
                string = i.split("a").pop()
                while(not string.replace(".","").isdigit() and len(string)>0):
                    string = string[1:]
                if string:
                    return string
        weight = re.compile(r'weight:\s*.{0,15}\s*:?\s*(?:\d+\.\d+|\d+)(?:k?gr?a?m?s?)',re.IGNORECASE)
        found = re.findall(weight, self.origdescription)
        #print "found ", found
        if found:
            for i in found:
                weight = re.compile(r'(?:\d+\.\d+|\d+)',re.IGNORECASE)
                foundnumber = re.findall(weight,str(i))
                if foundnumber:
                    #print 'returning' , foundnumber
                    return float(foundnumber[0]) 
                 
    def extractCurrent(self):
        desc = (self.name + " " + self.description).lower().replace(":","")
        name = ""
        names = ["max amps","max load", "max current","max. cur.","maximum current","max A","amp"]
        for i in names:
            if i in desc:
                name = i
        if name:
            string = desc.split(name)[1].split("a")[0]
            while not string[0:1].replace(".","").isdigit() and len(string)>0:
                string = string[1:]
            string = string.split("a")[0]
            while not string.replace(".","").isdigit() and len(string)>0:
                string = string[:-1]
            if string.replace(".","").isdigit():    
                return string 
        
        
    def extractVoltage(self):

        #print "trying"
        cells = re.compile(r'(?:cell?\scount|voltage|cells?)\s*:\s*.{0,10}\s*(?:\d+s?.\d+s?|\d+s?)',re.IGNORECASE)
        voltage = re.compile(r'(?:max\scurrent|voltage|power)\s*:?\s*.{0,10}\s*(?:\d+.\d+v|\d+v)',re.IGNORECASE)
        brushed = re.compile(r'\s?\d+V/\d+.\d+rpm',re.IGNORECASE)
        found = re.findall(cells, self.origdescription)
        if found:
            print found
            number = found.pop().split(" ").pop().replace(" ","").lower().replace("s",'')
            while not number.isdigit():
                number = number[1:]
            if number:
                return str(int(number) * 4.2)
            
        found = re.findall(voltage, self.origdescription)
        if found:
            print found
            number = found.pop().split(" ").pop()[0:-1].replace(" ","")
            while not number.replace(".","").isdigit():
                number = number[1:]
            if number:
                return number

        found = re.findall(brushed, self.origdescription)
        if found:
            print found
            #print "brushed!", found
            ##print "trying to get regex data"
            number = found.pop().split("rpm")[0].split("/")[0]
            number = re.findall(r"[-+]?\d+.\d+|\d+",number)[0].replace(",",'')
            ##print number
            while not number.replace(".","").isdigit() and len(number)>0:
                #print number
                number = number[1:]
            if number:
                ##print "found using regex!" , number
                #print number, "v"
                return number            
            
    def getExtendedData(self):
        url = root+ self.page
        #print self.name 

        soup = parseUrl(url)
        if soup:
            body = soup.find('table',width="246", border="0", cellspacing="1" ,cellpadding="2")
        
            if body:
                rows = body.findAll('tr')
                
                for row in rows:
                    tds = row.findAll('td')
                    attribute = tds[0].text.lower()
                    value = tds[1].text
                    if value.replace(".","").isdigit() and float(value)>0:
                        
                        
                        if 'kv' in attribute:
                            self.kv = value
                        elif 'weight' in attribute:
                            self.weight = value
                        elif 'current' in attribute:
                            self.maxCurrent = float(value)
                        elif 'resistance' in attribute:
                            self.resistance = value
                        elif 'voltage' in attribute:

                            self.maxVoltage = value
                        elif 'power' in attribute:
                            self.power = value

            data = soup.find('table',width='510px').tr.td
            self.origdescription = str(soup.find('table',width='510px')).replace('src="','src="' + root).replace("src='","src='" + root)
            self.id = str(soup.find('td',width=103)).split('wsSubframe.asp?idproduct=').pop().split(" ")[0]
            while not self.id.isdigit() and len(self.id)>0:
                self.id = self.id[:-1]
            bigimg = data.find('img')['src']
            if bigimg:
                self.bigimg = bigimg
            self.description =  self.name.lower() + " " + data.text.lower()
            if 'kv' in data.text  and not self.kv:
                self.kv = self.extract('kv')
            if 'rpm' in data.text and not self.kv:
                self.kv = self.extract('rpm')
            if not self.maxCurrent:
                self.maxCurrent = self.extractCurrent()
            if not self.weight:
                self.weight = self.extractWeight()
            if not self.maxVoltage:
                self.maxVoltage = self.extractVoltage()
            #print "kv -", self.kv, "  maxv =" , self.maxVoltage
            if not self.kv and self.maxVoltage:
                self.kv = self.extractKv()
                
    def deduceData(self):
        if not self.power:
            
            if self.maxCurrent and self.maxVoltage:
                #print "trying to deduce power"
                a = float(self.maxCurrent)
                v = float(self.maxVoltage)
                self.power = str(a*v)
                #print self.power
        if not self.maxCurrent:
            if self.power and self.maxVoltage:
                #print "trying to deduce current"
                self.maxCurrent = int(float(self.power)/float(self.maxVoltage))

        if not self.maxVoltage:
            if self.power and self.maxCurrent:
                #print "trying to deduce voltage"
                self.maxVoltage = int(float(self.power)/float(self.maxCurrent))

    def __init__(self,i):
        self.name = i.find('a' , onmouseout="this.style.color=''").text
        query = Motordb.objects.all().filter(name__iexact=self.name)
        if not query or (query and query[0].isIncomplete() ):
                print 'parsing ' + self.name
                for j in Motordb.objects.all().filter(name__iexact=self.name):
                    j.delete()
                self.img = i.find('img',border="1")['src']
                self.thrusts =[]
                self.nthrusts =[]
                self.maxThrust = 0
                self.kv = self.getKv()
                self.rating = self.getRating(i)
                self.page = i.find('a' , onmouseout="this.style.color=''")['href']
                self.price = float(i.find('font', style="font-size:16px").text[1:-6])
                self.getExtendedData()
                self.deduceData()
                self.getThrust()
                print 'V = ',self.maxVoltage
                print 'A = ',self.maxCurrent
                print 'W = ',self.weight
                print 'P = ',self.power
                print 'T = ',self.maxThrust 
                #print self.thrusts
                self.addToDb()
        else:
            print "not parsing " + self.name

        
        
        
        
