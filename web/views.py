'''
Created on Feb 24, 2012

@author: will
'''

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render_to_response, render

from web.models import Motor, Battery


def loadBatteries(request):
    itens = Battery.objects.all()
    unused = Battery.objects.all()
    page = 1
    revert = False
    if request.method == 'POST':
        print(request.POST)
        revert = request.POST['revert']
        itensp = itens.filter(name__icontains=request.POST['name'],
                              price__gt=int(request.POST['minPrice']),
                              price__lt=int(request.POST['maxPrice']),
                              weight__gt=int(request.POST['minWeight']),
                              weight__lt=int(request.POST['maxWeight']),
                              capacity__gt=int(request.POST['minCap']),
                              capacity__lt=int(request.POST['maxCap']),
                              heigth__gt=int(request.POST['minHeight']),
                              heigth__lt=int(request.POST['maxHeight']),
                              width__gt=int(request.POST['minWidth']),
                              width__lt=int(request.POST['maxWidth']),
                              length__gt=int(request.POST['minLength']),
                              length__lt=int(request.POST['maxLength']),
                              cells__gt=int(request.POST['minCells']),
                              cells__lt=int(request.POST['maxCells'])
                              )

        itens = itensp.order_by(request.POST['sort'])

        unused = unused.exclude(pk__in=itens).order_by(request.POST['sort'])
        page = request.POST['page']

    else:
        itens = itens.order_by('name')
        unused = []
    if revert == 'false':
        paginator = Paginator(itens, 30)
    else:
        paginator = Paginator(unused, 30)
    itens2 = paginator.page(page)
    amm = "Found " + str(len(itens)) + " itens. of " + str(len(itens) + len(unused))

    return render(request, 'batteries.html', {'amm': amm, 'itens': itens2})


def loadMotors(request):
    itens = Motor.objects.all()
    unused = Motor.objects.all()
    page = 1
    revert = False
    if request.method == 'POST':
        print(request.POST)
        revert = request.POST['revert']
        itensp = itens.filter(name__icontains=request.POST['name'],
                              price__gt=int(request.POST['minPrice']),
                              price__lt=int(request.POST['maxPrice']),
                              kv__gt=int(request.POST['minKv']),
                              kv__lt=int(request.POST['maxKv']),
                              rating__lt=int(request.POST['maxRating']),
                              rating__gt=int(request.POST['minRating']),
                              weight__gt=int(request.POST['minWeight']),
                              weight__lt=int(request.POST['maxWeight']), )

        itens = itensp.filter(maxCurrent__lt=int(request.POST['maxCur']),
                              maxVoltage__lt=int(request.POST['maxVol']),
                              power__lt=int(request.POST['maxPower']),
                              maxThrust__lt=int(request.POST['maxThrust']),
                              maxCurrent__gt=int(request.POST['minCur']),
                              maxVoltage__gt=int(request.POST['minVol']),
                              power__gt=int(request.POST['minPower']),
                              maxThrust__gt=int(request.POST['minThrust'])
                              )

        if request.POST['incomplete'] == "true":
            itens = itens | itensp.filter(maxCurrent=None,
                                          maxVoltage__lt=int(request.POST['maxVol']),
                                          power__lt=int(request.POST['maxPower']),
                                          maxThrust__lt=int(request.POST['maxThrust']),
                                          maxVoltage__gt=int(request.POST['minVol']),
                                          power__gt=int(request.POST['minPower']),
                                          maxThrust__gt=int(request.POST['minThrust']))

            itens = itens | itensp.filter(maxCurrent__lt=int(request.POST['maxCur']),
                                          maxVoltage=None,
                                          power__lt=int(request.POST['maxPower']),
                                          maxThrust__lt=int(request.POST['maxThrust']),
                                          maxCurrent__gt=int(request.POST['minCur']),
                                          power__gt=int(request.POST['minPower']),
                                          maxThrust__gt=int(request.POST['minThrust']))

            itens = itens | itensp.filter(maxCurrent__lt=int(request.POST['maxCur']),
                                          maxVoltage__lt=int(request.POST['maxVol']),
                                          power__lt=int(request.POST['maxPower']),
                                          maxThrust=None,
                                          maxCurrent__gt=int(request.POST['minCur']),
                                          maxVoltage__gt=int(request.POST['minVol']),
                                          power__gt=int(request.POST['minPower']))

            itens = itens | itensp.filter(maxCurrent__lt=int(request.POST['maxCur']),
                                          maxVoltage__lt=int(request.POST['maxVol']),
                                          power=None,
                                          maxThrust__lt=int(request.POST['maxThrust']),
                                          maxCurrent__gt=int(request.POST['minCur']),
                                          maxVoltage__gt=int(request.POST['minVol']),
                                          maxThrust__gt=int(request.POST['minThrust']))

        itens = itens.order_by(request.POST['sort'])

        unused = unused.exclude(pk__in=itens).order_by(request.POST['sort'])
        page = request.POST['page']

    else:
        itens = itens.order_by('name')
        unused = []
    if revert == 'false':
        paginator = Paginator(itens, 30)
    else:
        paginator = Paginator(unused, 30)
    itens2 = paginator.page(page)
    amm = "Found " + str(len(itens)) + " itens. of " + str(len(itens) + len(unused))

    return render(request, 'motors.html', {'amm': amm, 'itens': itens2})


def motorDesc(request):
    obj = None
    if request.method == 'POST':
        obj = Motor.objects.all().filter(name__iexact=request.POST['name'])
    elif request.method == 'GET':
        obj = Motor.objects.all().filter(name__iexact=request.GET['name'])

    if obj:
        if obj[0]:
            string = obj[0].description
            return HttpResponse(string)
    return HttpResponse("NONE" + request.POST['name'])


def batDesc(request):
    obj = None
    if request.method == 'POST':
        obj = Battery.objects.all().filter(name__iexact=request.POST['name'])
    elif request.method == 'GET':
        obj = Battery.objects.all().filter(name__iexact=request.GET['name'])

    if obj:
        if obj[0]:
            string = obj[0].description
            return HttpResponse(string)
    return HttpResponse("NONE" + request.POST['name'])


def home(request):
    return render_to_response('home.html')
