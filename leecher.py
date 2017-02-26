'''
Created on Nov 9, 2011

@author: will
'''

# -*- coding: UTF-8 -*-    

import settings
from django.core.management import setup_environ
setup_environ(settings)
from crawler.motor import Motor

from crawler.urlfetcher import parseUrl

#!/usr/bin/env python


motors1 = ['uh_listCategoriesAndProducts.asp?idCategory=523']

motors = ['uh_listCategoriesAndProducts.asp?idCategory=518',
          'uh_listCategoriesAndProducts.asp?idCategory=519',    
          'uh_listCategoriesAndProducts.asp?idCategory=520',
          'uh_listCategoriesAndProducts.asp?idCategory=521',
          'uh_listCategoriesAndProducts.asp?idCategory=522',
          'uh_listCategoriesAndProducts.asp?idCategory=523',
          'uh_listCategoriesAndProducts.asp?idCategory=513',
          'uh_listCategoriesAndProducts.asp?idCategory=514',
          'uh_listCategoriesAndProducts.asp?idCategory=515',
          'uh_listCategoriesAndProducts.asp?idCategory=516']
        

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
        myproducts = []
        finds = soup.findAll('table', width="563", border="0", cellspacing="0", cellpadding="0")
        print len(finds)
        for i,j in zip(finds,finds[1:])[::2]: #little hack to drop every repeated entry
		try:
                	myproducts.append(Motor(i))
		except:
			print "could not read motor! {0}".format(str(i))
        return myproducts
    
    
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
    return getProducts(motors)

getMotors()
