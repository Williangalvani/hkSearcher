'''
Created on Feb 24, 2012

@author: Will
'''
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, URLError
import socket

root = 'http://www.hobbyking.com/hobbyking/store/'
def parseUrl(url):
    if not root in url:
        url = root + url
    soup = None
    while(not soup):
        try:
            #print 'fetching'
            soup = BeautifulSoup(urlopen(url,timeout=10 ).read())
            #print 'parsed ' + url
            return soup
        except URLError, e:
            print e
        except socket.error, e:
            print e

    return soup