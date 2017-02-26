'''
Created on Feb 24, 2012

@author: Will
'''
from bs4 import BeautifulSoup
from urllib import request
import socket



def parseUrl(url):
    soup = None
    while (not soup):
        try:
            # print 'fetching'
            soup = BeautifulSoup(request.urlopen(url, timeout=10).read())
            # print 'parsed ' + url
            return soup
        except socket.error as e:
            print(e)

    return soup
