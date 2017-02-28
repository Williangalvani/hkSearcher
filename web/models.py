'''
Created on Feb 24, 2012

@author: will
'''


from django.db import models
from web import HTML


class Motor(models.Model):
    """
    Represents the model on the database.
    """
    kv = models.IntegerField(null=True, blank=True)
    name = models.CharField(max_length=200)
    price = models.FloatField()
    rating = models.FloatField(null=True, blank=True)
    img = models.CharField(max_length=30, null=True, blank=True)
    bigimg = models.CharField(max_length=30, null=True, blank=True)
    page = models.CharField(max_length=20, null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_current = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    resistance = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_thrust = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    power = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    max_voltage = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=3000, null=True, blank=True)

    def data_table(self):
        """
        render model as html <table>
        :return:
        """
        table_data = [['Name:', "<a href='" + self.page + "'>" + self.name + "</a>"]]
        if self.kv:
            table_data.append(['kv:', self.kv])
        table_data.append(['Price:', self.price])
        table_data.append(['Rating:', self.rating])
        if self.weight:
            table_data.append(['Weight:', self.weight])
        if self.resistance:
            table_data.append(['Resistance:', self.resistance])
        if self.max_current:
            table_data.append(['Max Current:', self.max_current])
        if self.max_voltage:
            table_data.append(['Max Voltage:', self.max_voltage])
        if self.power:
            table_data.append(['Power:', self.power])
        htmlcode = HTML.table(table_data)
        return htmlcode

    def is_incomplete(self):
        """
        Checks if all fields are filled
        :return: any of the fields is None
        """
        if not self.max_current:
            return True
        if not self.max_voltage:
            return True
        if not self.weight:
            return True
        if not self.power:
            return True
        if not self.kv or self.kv > 30000:
            return True
        if not self.max_thrust:
            return True

        # print " complete, ignoring" , self.name
        return True

    def display_line(self):
        """
        render motor as html <tr> tags for the listing
        :return: str  "<tr>....</tr>"
        """
        table_data = "<tr><td><img style='height:84px;width:115px' src='" + self.img + "'></img>"
        table_data = table_data + '''</td class='span4'><td><a class='motorlink'  href="#"  link=' ''' + self.page + "'>" + self.name + "</a><br><br><br><a target='_blank' href='" + self.page + "'>View At HK <i class='icon-share-alt'></i></a>"
        table_data = table_data + "</td><td> " + str(self.kv)
        table_data = table_data + " rpm/v</td><td> USD " + str(self.price)
        table_data = table_data + "</td><td> " + str(self.rating)
        table_data = table_data + " Stars</td><td> " + str(self.weight)
        if self.resistance:
            table_data = table_data + "g </td><td> " + str(self.resistance)
        else:
            table_data = table_data + "g </td><td> N/A"
        if self.max_current:
            table_data = table_data + "</td><td> " + str(self.max_current) + "A "
        else:
            table_data = table_data + "</td><td> N/A "
        table_data = table_data + "</td><td> " + str(self.max_voltage)
        if self.max_thrust:
            table_data = table_data + "V</td><td> " + str(self.max_thrust) + "g     "
        else:
            table_data = table_data + "V</td><td> N/A "
        table_data = table_data + "</td><td> " + str(self.power) + "W</td></tr>"
        return table_data


class Battery(models.Model):
    img = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    page = models.CharField(max_length=1000)
    heigth = models.FloatField()
    width = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    crating = models.FloatField(null=True, blank=True)
    cchargerating = models.FloatField(null=True, blank=True)
    rating = models.FloatField()
    capacity = models.FloatField()
    cells = models.IntegerField(null=True, blank=True)
    price = models.FloatField()
    weight = models.FloatField(null=True, blank=True)
    description = models.CharField(max_length=3000)

    def display_line(self):
        table_data = "<tr><td><img style='height:84px;width:115px' src='" + self.img + "'></img>"
        table_data = table_data + '''</td class='span4'><td><a class='motorlink'  href="#"  link="" ''' + \
                     self.name + "'>" + self.name + "</a><br><br><br><a target='_blank' href='" + \
                     self.page + "'>View At HK <i class='icon-share-alt'></i></a>"
        table_data = table_data + "</td><td> USD " + str(self.price)
        table_data = table_data + "</td><td> " + str(self.cells)
        table_data = table_data + "S</td><td> " + str(self.capacity)
        table_data = table_data + "mah</td><td> " + str(self.rating)
        table_data = table_data + "</td><td> " + str(self.weight)
        table_data = table_data + "g</td><td> " + str(self.heigth)
        table_data = table_data + "mm</td><td> " + str(self.length)
        table_data = table_data + " mm</td><td> " + str(self.width)
        table_data = table_data + " mm</td><td> " + str(self.crating)
        table_data = table_data + " C</td><td> " + str(self.cchargerating) + "C</td></tr>"

        return table_data
