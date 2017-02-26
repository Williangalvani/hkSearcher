'''
Created on Nov 9, 2011

@author: will
'''

# -*- coding: UTF-8 -*-    

import settings
from django.core.management import setup_environ
setup_environ(settings)
from crawler.battery import Battery

from crawler.urlfetcher import parseUrl

#!/usr/bin/env python

batteries = ['__86__85__LiPo_LiFe_NiMH_Battery-Li_Poly_All_brands_.html']
        

root = 'http://www.hobbyking.com/hobbyking/store/'

print "begin"

def getNextPage(soup):
    form = soup.find('input',type='BUTTON',value=">")
    if form:
        text = form.parent.text
        page = text.split("document.location.href=").pop()[1:-4].replace(";","")
        return page
    return None

def getProducts(adresses):
    products = []
    
    def extract(soup):

        finds = soup.findAll('table', width="563", border="0", cellspacing="0", cellpadding="0")
        print len(finds)
        for i,j in zip(finds,finds[1:])[::2]: #little hack to drop every repeated entry
                b = Battery(i)
                del(b)
                
    
    
    for adress in adresses:        
        url = root + adress
        soup = parseUrl(url)
        #products.extend(extract(soup))
        extract(soup)
        while(getNextPage(soup)):
            url = root+ getNextPage(soup)
            soup = parseUrl(url)
            #products.extend(extract(soup))            
            extract(soup)
    return products


def getMotors():
    return getProducts(batteries)

getMotors()
