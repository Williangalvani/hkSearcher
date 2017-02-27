from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        '''
        Created on Nov 9, 2011

        @author: will
        '''

        # -*- coding: UTF-8 -*-


        from bs4 import BeautifulSoup
        from urllib import request
        from crawler.motor import Motor
        from crawler.urlfetcher import parseUrl

        # !/usr/bin/env python


        motors1 = ['https://hobbyking.com/en_us/electric-motors-1/inrunners-by-size/12-24mm.html']

        root = ''

        print("begin")

        def getNextPage(soup):
            form = soup.find('input', type='BUTTON', value=">")
            if form:
                text = form.parent.text
                page = text.split("document.location.href=").pop()[1:-4].replace(";", "")
                return page
            return None

        def getProducts(adresses):
            products = []

            def extract(soup):
                myproducts = []
                finds = soup.findAll('li', class_="item")
                print(len(finds))
                for i, j in zip(finds, finds[1:]):  # little hack to drop every repeated entry
                    # try:
                    myproducts.append(Motor(i))
                    # except:
                    #    print("could not read motor! {0}".format(str(i)))
                return myproducts

            for adress in adresses:
                url = root + adress
                print(url)
                soup = parseUrl(url)
                # products.extend(extract(soup))
                extract(soup)
                while (getNextPage(soup)):
                    url = root + getNextPage(soup)
                    soup = parseUrl(url)
                    # products.extend(extract(soup))
                    extract(soup)
            return products

        def getMotors(links):
            return getProducts(links)

        import re
        MATCH_ALL = r'.*'

        def like(string):
            """
            Return a compiled regular expression that matches the given
            string with any prefix and postfix, e.g. if string = "hello",
            the returned regex matches r".*hello.*"
            """
            string_ = string
            if not isinstance(string_, str):
                string_ = str(string_)
            regex = MATCH_ALL + re.escape(string_) + MATCH_ALL
            return re.compile(regex, flags=re.DOTALL)

        def find_by_text(soup, text, tag, **kwargs):
            """
            Find the tag in soup that matches all provided kwargs, and contains the
            text.

            If no match is found, return None.
            If more than one match is found, raise ValueError.
            """
            elements = soup.find_all(tag, **kwargs)
            matches = []
            for element in elements:
                if element.find(text=like(text)):
                    matches.append(element)
            return matches

        def getSubPages(link):
            page = BeautifulSoup(request.urlopen(link, timeout=10).read(), "lxml")
            links = page.find_all("a", class_="brandOuterLink")
            sublinks = [link["href"] for link in links]
            print(sublinks)
            return sublinks

        def getPages():

            home = BeautifulSoup(request.urlopen("https://hobbyking.com/", timeout=10).read(), "lxml")
            electric_motor_links = find_by_text(home, "Electric Motors", "a")

            parents = [link.parent for link in electric_motor_links]
            print("Parents:", len(parents))

            lis = []
            for parent in parents:
                lis.extend(parent.find_all("li", class_='level1'))
            print(len(lis))
            links = []
            for li in lis:
                links.append(li.find("a")["href"])
            level0 = links

            sublinks = []
            for link in level0:
                sublinks.extend(getSubPages(link))

            return links + sublinks

        # getPages()
        getMotors(getPages())
