'''
Created on Feb 25, 2012

@author: will

'''

from django import forms


class SearchForm(forms.Form):
    field = forms.ChoiceField(label='', choices=(
        ('name', 'Name'),
        ('kv', 'Kv'),
        ('price', 'Price'),
        ('rating', 'Rating'),
        ('weight', 'Weight'),
        ('resistance', 'Resistance'),
        ('max_current', 'Max current'),
        ('max_voltage', 'Max Voltage'),
        ('power', 'Power')))
