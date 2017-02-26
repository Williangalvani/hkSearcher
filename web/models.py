'''
Created on Feb 24, 2012

@author: will
'''

from django.db import models

import HTML
import re

root = 'http://www.hobbyking.com/hobbyking/store/'

class Motor(models.Model):
    kv = models.IntegerField(max_length=20,null=True,blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    rating = models.IntegerField(max_length=20,null=True,blank=True)
    img = models.CharField(max_length=30,null=True,blank=True)
    bigimg = models.CharField(max_length=30,null=True,blank=True)
    page = models.CharField(max_length=20,null=True,blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    maxCurrent = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    resistance = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    maxThrust = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    
    power = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    maxVoltage = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=3000)
    
    def extractThrust(self,source):
        thrust =  re.compile(r'(?:Thrust|Pulls?)\s*:?\s*[^ ^0-9]{0,10}\s*(?:(?:\d+.\d+|\d+).?\s*)+(?:k?gr?a?m?s?|oz)',re.IGNORECASE)
        thrust2 = re.compile(r'(?:\d+.\d+|\d+)+(?:k?gr?a?m?s?|oz)\s?.{0,2}\sthrust',re.IGNORECASE)
        
        found = []
        for regexp in [thrust,thrust2]:
            found.append(re.findall(regexp, source))
        numbers = []
        
        for i in found:
            s = str(i)
            factor = 1
            #print i
            if "kg" in s:
                factor = 1000
            if "oz"in s:
                factor = 28.34
            strings = [s]
            if ", " in s:
                strings = s.split(", ")
            for string in strings:
                all = re.findall(r"[-+]?\d*\.\d+|\d+",string)
                for number in all:
                    if number.replace('.','').isdigit():
                        numbers.append(float(number)*factor)
        if numbers:
            print max(numbers)
            self.maxThrust = max(numbers)
            self.save()
            print self.maxThrust
        else:
            return None
    
    def getEff(self):
        if self.maxThrust and self.power:
            return self.maxThrust/self.power
        return None
    
           
    def extractVoltage(self):
        string = self.description.lower().split("Voltage")[0]
        while not string[0:1].replace(".","").isdigit():
            string = string[1:]
        string = string.split("v")[0]
        if string.replace(".","").isdigit():
            return string 
        
        cells = re.compile(r'(?:cell\scount|voltage)\s*:\s*.{1,10}\s*(?:\d+s?.\d+s|\d+s)',re.IGNORECASE)
        voltage = re.compile(r'(?:max\scurrent|voltage)\s*:\s*.{1,10}\s*(?:\d+.\d+v|\d+v)',re.IGNORECASE)
        brushed = re.compile(r'\s?\d+V/\d+.\d+rpm',re.IGNORECASE)
        found = re.findall(cells, self.description)
        if found:
            number = found.pop().split(" ").pop()[0:-1].replace(" ","")
            while not number.isdigit():
                number = number[1:]
            if number:
                return str(int(number) * 4.2)
            
        found = re.findall(voltage, self.description)
        if found:
            number = found.pop().split(" ").pop()[0:-1].replace(" ","")
            while not number.replace(".","").isdigit():
                number = number[1:]
            if number:
                return number

        found = re.findall(brushed, self.description)
        if found:
            print "brushed!", found
            #print "trying to get regex data"
            number = found.pop().lower().split('v')[0]
            number = re.findall(r"[-+]?\d*\.\d+|\d+",number)[0]
            
            while not number.replace(".","").isdigit() and len(number)>0:
                print number
                number = number[1:]
            if number:
                #print "found using regex!" , number
                print number, "v"
                return number            
    
    
    def extractKv(self):
        brushed = re.compile(r'\s?\d+V/\d+.\d+rpm',re.IGNORECASE)
        found = re.findall(brushed, self.description)
        if found:
            number = found.pop().split("rpm")[0].split("/").pop()
            number = re.findall(r"[-+]?\d+.\d+|\d+",number)[0].replace(",",'')
            #print number
            while not number.isdigit() and len(number)>0:
                number = number[1:]
            if number:
                if self.maxVoltage:
                    return int(float(number) / float(self.maxVoltage))

    
    def dataTable(self):
        table_data = [['Name:',  "<a href='" + root+ self.page + "'>" + self.name + "</a>"]]
        if self.kv:
            table_data.append(['kv:',       self.kv])
        table_data.append(['Price:',   self.price])        
        table_data.append(['Rating:',     self.rating])
        if self.weight:
            table_data.append(['Weight:',     self.weight])
        if self.resistance:
            table_data.append(['Resistance:',     self.resistance])
        if self.maxCurrent:
            table_data.append(['Max Current:',     self.maxCurrent])
        if self.maxVoltage:
            table_data.append(['Max Voltage:',     self.maxVoltage])
        if self.power:
            table_data.append(['Power:',     self.power])
        htmlcode = HTML.table(table_data)
        return htmlcode
    
    def isIncomplete(self):
        if not self.maxCurrent:
            return True
        if not self.maxVoltage:
            return True
        if not self.weight:
            return True
        if not self.power:
            return True
        if not self.kv or self.kv > 30000:
            return True
        if not self.maxThrust:
            return True
        
        #print " complete, ignoring" , self.name
        return True
    
    
    def displayLine(self):
        table_data = "<tr><td><img style='height:84px;width:115px' src='" + root + self.img + "'></img>"
        table_data = table_data + '''</td class='span4'><td><a class='motorlink'  href="#"  link=' ''' + root + self.page + "'>"   + self.name + "</a><br><br><br><a target='_blank' href='" + root+ self.page + "'>View At HK <i class='icon-share-alt'></i></a>"
        table_data=table_data + "</td><td> " +   str(self.kv)
        table_data=table_data + " rpm/v</td><td> USD " +str(self.price   )    
        table_data=table_data + "</td><td> " + str(self.rating)
        table_data=table_data +" Stars</td><td> " +  str(self.weight)
        if self.resistance:
            table_data=table_data + "g </td><td> " +    str(self.resistance)
        else:
            table_data=table_data + "g </td><td> N/A"
        if self.maxCurrent:
            table_data=table_data +"</td><td> " + str(self.maxCurrent) + "A "
        else:
            table_data=table_data +"</td><td> N/A " 
        table_data=table_data + "</td><td> " +     str(self.maxVoltage)
        if self.maxThrust:
            table_data=table_data +"V</td><td> " + str(self.maxThrust) + "g     "
        else:
            table_data=table_data +"V</td><td> N/A " 
        table_data=table_data +"</td><td> " +  str(self.power) + "W</td></tr>"
        return table_data
    


class Battery(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    page = models.CharField(max_length=1000)
    heigth = models.FloatField()
    width = models.FloatField(null=True,blank=True)
    length = models.FloatField(null=True,blank=True)
    crating = models.FloatField(null=True,blank=True)
    cchargerating = models.FloatField(null=True,blank=True)
    rating = models.FloatField()
    capacity = models.FloatField()
    cells = models.IntegerField(null=True,blank=True)
    price = models.FloatField()
    weight = models.FloatField(null=True,blank=True)
    description = models.CharField(max_length=3000)
    
    
    def displayLine(self):
        table_data = "<tr><td><img style='height:84px;width:115px' src='" + root + self.img + "'></img>"
        table_data = table_data + '''</td class='span4'><td><a class='motorlink'  href="#"  link="" ''' + root +  self.name  + "'>"   + self.name + "</a><br><br><br><a target='_blank' href='" + root+ self.page + "'>View At HK <i class='icon-share-alt'></i></a>"
        table_data=table_data + "</td><td> USD " +str(self.price   )    
        table_data=table_data + "</td><td> " + str(self.cells)
        table_data=table_data + "S</td><td> " + str(self.capacity)
        table_data=table_data + "mah</td><td> " + str(self.rating)
        table_data=table_data + "</td><td> " + str(self.weight)
        table_data=table_data + "g</td><td> " + str(self.heigth)
        table_data=table_data + "mm</td><td> " + str(self.length)
        table_data=table_data +" mm</td><td> " +  str(self.width)
        table_data=table_data +" mm</td><td> " +  str(self.crating)
        table_data=table_data +" C</td><td> " +  str(self.cchargerating) + "C</td></tr>"
        
        return table_data
    