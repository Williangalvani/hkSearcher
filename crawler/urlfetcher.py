'''
Created on Feb 24, 2012

@author: Will
'''
import socket
from urllib import request

from bs4 import BeautifulSoup


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
