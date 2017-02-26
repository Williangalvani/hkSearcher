'''
Created on Feb 24, 2012

@author: Will
'''
from urlfetcher import parseUrl
from hksearcher.web.models import Battery as Batterydb
import re
import string

from hksearcher.crawler import urlfetcher

root = 'http://www.hobbyking.com/hobbyking/store/'


class Battery(object):
    heigth = None
    page = None
    width = None
    length = None
    crating = None
    cchargerating = None
    rating = None
    capacity = None
    cells = None
    price = None
    weight = None
    description = None

    def getReviews(self):
        if not self.reviews:
            self.reviews = parseUrl('reviewsSubframe.asp?idproduct=' + self.id + "&more=1")
        return self.reviews

    def addToDb(self):
        if self.capacity:
            dbbat = Batterydb()
            dbbat.name = self.name
            try:
                dbbat.heigth = float(self.heigth)
            except:
                dbbat.heigth = 0
            dbbat.width = self.width
            dbbat.length = self.length
            dbbat.crating = self.crating
            dbbat.cchargerating = self.cchargerating
            dbbat.rating = self.rating
            dbbat.capacity = self.capacity
            dbbat.page = self.page
            dbbat.cells = self.cells
            dbbat.img = self.img
            dbbat.price = self.price
            dbbat.weight = self.weight
            dbbat.description = self.origdescription
            dbbat.save()

    def __str__(self):
        return "\n\n" + str(self.name) + "  \npage = " + str(self.page) + "  \nkv = " + str(
            self.kv) + " \nrating = " + str(self.rating) + " \nprice = " + str(self.price) + " \nPower = " + str(
            self.power) + " \nweight = " + str(self.weight)

    def getRating(self, i):
        ratingstring = i.find('td', background="images/new07/bgd05.jpg").img['src']
        return ratingstring.split("/").pop()[0:1]

    def getExtendedData(self):
        url = root + self.page  # print self.name

        soup = parseUrl(url)
        if soup:
            body = soup.find('table', width="246", border="0", cellspacing="1", cellpadding="2")

            if body:
                self.description = body
                rows = body.findAll('tr')

                for row in rows:
                    tds = row.findAll('td')
                    attribute = tds[0].text.lower()
                    value = tds[1].text
                    if value.replace(".", "").isdigit() and float(value) > 0:

                        if 'width' in attribute:
                            self.width = value
                        if 'config' in attribute:
                            self.cells = value
                        if 'capacity' in attribute:
                            self.capacity = value
                        elif 'weight' in attribute:
                            self.weight = value
                        elif 'height' in attribute:
                            self.heigth = value
                        elif 'length' in attribute:
                            self.length = value
                        elif 'discharge' in attribute:
                            self.crating = value
                        elif 'rate' in attribute:
                            self.cchargerating = value

            data = soup.find('table', width='510px').tr.td
            self.origdescription = str(soup.find('table', width='510px')).replace('src="', 'src="' + root).replace(
                "src='", "src='" + root)
            self.id = str(soup.find('td', width=103)).split('wsSubframe.asp?idproduct=').pop().split(" ")[0]
            while not self.id.isdigit() and len(self.id) > 0:
                self.id = self.id[:-1]
            bigimg = data.find('img')['src']
            if bigimg:
                self.bigimg = bigimg

    def __init__(self, i):
        print("got here")
        self.name = i.find('a', onmouseout="this.style.color=''").text
        query = Batterydb.objects.all().filter(name__iexact=self.name)
        if not query or (query and (query[0].width == query[0].length)):
            print('parsing ' + self.name)
            for j in Batterydb.objects.all().filter(name__iexact=self.name):
                j.delete()
            self.img = i.find('img', border="1")['src']
            self.rating = self.getRating(i)
            self.page = i.find('a', onmouseout="this.style.color=''")['href']
            self.price = float(i.find('font', style="font-size:16px").text[1:-6])
            self.getExtendedData()

            print(self.cells, "S ", self.capacity, "mah  ", self.weight, "g", self.heigth, self.width, self.length,
                  self.page)
            # print self.thrusts
            self.addToDb()
        else:
            print("not parsing " + self.name)
