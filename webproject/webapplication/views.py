from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpRequest, JsonResponse
from .models import *
from django.urls import reverse
from django.views import generic
from django.core import serializers
from . import floor
from .forms import Addfloor_form
import json


# Create your views here. request function is necessary here.
# Request contain methods(POST ,GET, FILES), path, path_info, cookies
# RESTful GET POST COOKIES
class IndexView(generic.ListView):
    template_name = 'webapplication/index.html'
    context_object_name = 'latest_question_list'


class DetailView(generic.DetailView):
    model = Question
    template_name = 'webapplication/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'webapplication/results.html'


class AddfloorView(generic.DetailView):
    model = Choice
    template_name = 'webapplication/addfloor'


# Index page: display a table for all simulation information
def index(request: HttpRequest):
    context = {}
    simulationInfo = SimulationInfo.objects.all()
    buildingInfo = BuildingInfo.objects.all()
    context['simulation'] = simulationInfo
    context['building'] = buildingInfo
    return render(request, 'webapplication/index.html', context)


# Not used yet
def function_list(request: HttpRequest):
    all_choice_list = Choice.objects.all()
    return render(request,
                  'webapplication/function_list.html',
                  {'all_list': all_choice_list})


# Not used yet. (try except method)
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})


# Add floor function page. 1. GET html page with a input form; 2. POST retrieve form data and process
# 3. Display simulation results
def addfloor(request: HttpRequest):
    context = {}

    if (request.method == "GET"):
        return render(request, 'webapplication/addfloor.html')
    else:
        # ----retrive message from previous page
        nfloor = request.POST.get('nfloor')
        cheight = request.POST.get('hceiling')
        file_obj = request.FILES.get('uploadFile')
        # File operation: 把缓存中文件读取到本地，当前文件夹
        with open(file_obj.name, 'wb') as f:
            for i in file_obj:
                f.write(i)
        print(request.FILES)

        # context['x1']=nfloor
        # context['x2']=cheight
        # print('recveied value %s and %s' % (nfloor, cheight))
        # # 加载数据模型
        # # results = floor.main(int(nfloor), float(cheight))
        # # context['message'] = results
        # referer = request.META.get('HTTP_REFERER')   #reference url to previous page

        return render(request, 'webapplication/addfloor.html', context)


def showAll(request: HttpRequest):
    jlist = []
    sInfo = SimulationInfo.objects.all()
    cElec = ConsumpElectricCooling.objects.filter(bid='52')
    for i in cElec:
        nameAndMonths = {}
        for si in sInfo:
            if i.sid == si.id:
                nameAndMonths['name'] = si.simulation_option
        value_list = [i.month1, i.month2, i.month3, i.month4, i.month5, i.month6, i.month7, i.month8, i.month9,
                      i.month10, i.month11, i.month12]
        nameAndMonths['value'] = value_list
        jlist.append(nameAndMonths)

    print('----prints jlist----')
    print(json.dumps(jlist))

    it_list = ['Month1', 'Month2', 'Month3', 'Month4', 'Month5', 'Month6', 'Month7', 'Month8', 'Month9', 'Month10',
               'Month11', 'Month12']
    val_list = [0, 0, 1, 1, 10, 1, 1, 1, 2, 0, 0, 0]

    if request.method == "GET":
        return render(request, 'webapplication/results.html', {'JList': json.dumps(jlist)})

    else:
        numb = request.POST.get('numbers')
        context = {}
        context['res'] = numb
        return render(request, 'webapplication/results.html', context)


# Consider visualize an example model, single zone/ Consumption, and power
# Consumption is displayed in line graph respectively in 6 categories and a sum
# Power is displayed in one bar graph
def building52(request):
    sInfo = SimulationInfo.objects.all()
    try:
        cElec = ConsumpElectricCooling.objects.filter(bid='52')
        cHotWater = ConsumpDomesticHotWater.objects.filter(bid='52')
        cEquip = ConsumpEquipmentTenant.objects.filter(bid='52')
        cFuel = ConsumpFuelHeating.objects.filter(bid='52')
        cHvac = ConsumpHvac.objects.filter(bid='52')
        cLight = ConsumpLightingFacility.objects.filter(bid='52')
        pElec = PkPowerElectricCooling.objects.filter(bid='52')
        pHotWater = PkPowerDomesticHotWater.objects.filter(bid='52')
        pFuel = PkPowerFuelHeating.objects.filter(bid='52')
        pHvac = PkPowerHvac.objects.filter(bid='52')
        pLight = PkPowerLightingFacility.objects.filter(bid='52')
        pEquip = PkPowerLightingFacility.objects.filter(bid='52')

    except (KeyError, Choice.DoesNotExist):
        # Reload keyError message into the page.
        return render(request, 'webapplication/building52.html',
                      {'error_message': "Incorrect building id selection.", })

    # Convert QuerySet into array and dictionary, then to json form
    def consumpToList(obj):
        jlist = []
        for i in obj:
            nameAndMonths = {}
            for si in sInfo:
                if i.sid == si.id:
                    nameAndMonths['name'] = si.simulation_option
            value_list = [i.month1, i.month2, i.month3, i.month4, i.month5, i.month6, i.month7, i.month8, i.month9,
                          i.month10, i.month11, i.month12]
            nameAndMonths['value'] = value_list
            jlist.append(nameAndMonths)
        return jlist

    cElec_list = consumpToList(cElec)
    cEquip_list = consumpToList(cEquip)
    cFuel_list = consumpToList(cFuel)
    cHvac_list = consumpToList(cHvac)
    cHotWater_list = consumpToList(cHotWater)
    cLight_list = consumpToList(cLight)

    # Sum of all consumptions
    sum_list = consumpToList(cElec)
    for i in range(len(sum_list)):
        for j in range(12):
            sum_list[i]['value'][j] = cElec_list[i]['value'][j] + cEquip_list[i]['value'][j] + \
                                      cHotWater_list[i]['value'][j] + \
                                      cHvac_list[i]['value'][j] + cLight_list[i]['value'][j] + cFuel_list[i]['value'][j]

    # Convert QuerySet of Power into array and dictionary
    power_legand_list = []
    power_values = []
    for i in range(len(pLight)):
        for si in sInfo:
            if pElec[i].sid == si.id:
                power_legand_list.append(si.simulation_option)
        sublist = [pElec[i].pk_power, pEquip[i].pk_power, pLight[i].pk_power, pFuel[i].pk_power, pHotWater[i].pk_power,
                   pHvac[i].pk_power]
        power_values.append(sublist)

    # Context in json form
    context = {'cElec': json.dumps(cElec_list), 'cEquip': json.dumps(cEquip_list),
               'cFuel': json.dumps(cFuel_list), 'cHvac': json.dumps(cHvac_list),
               'cHotWater': json.dumps(cHotWater_list), 'cLight': json.dumps(cLight_list),
               'cSum': json.dumps(sum_list), 'power_legends': json.dumps(power_legand_list),
               'power_values': json.dumps(power_values)}

    return render(request, 'webapplication/building52.html', context)


# The form receives max window width and simulation times
# The initial window width is 1m for all orientations
def wwr(request: HttpRequest):

    if (request.method == "GET"):
        return render(request, 'webapplication/wwr.html')

    else:
        # retrive data from form, ajax
        # Below is under modification
        simu_time = request.POST.get('simu_time')
        max_width = request.POST.get('largest_width')
        print(simu_time)
        print(max_width)

        sInfo = SimulationInfo.objects.all()
        pElec = PkPowerElectricCooling.objects.filter(bid='52')
        pHotWater = PkPowerDomesticHotWater.objects.filter(bid='52')
        pFuel = PkPowerFuelHeating.objects.filter(bid='52')
        pHvac = PkPowerHvac.objects.filter(bid='52')
        pLight = PkPowerLightingFacility.objects.filter(bid='52')
        pEquip = PkPowerLightingFacility.objects.filter(bid='52')
        # Convert QuerySet of Power into array and dictionary
        power_legand_list = []
        power_values = []
        for i in range(len(pLight)):
            for si in sInfo:
                if pElec[i].sid == si.id:
                    power_legand_list.append(si.simulation_option)
            sublist = [pElec[i].pk_power, pEquip[i].pk_power, pLight[i].pk_power, pFuel[i].pk_power,
                       pHotWater[i].pk_power, pHvac[i].pk_power]
            power_values.append(sublist)

        # results = floor.main(int(nfloor), float(cheight))
        context = {'power_legends': json.dumps(power_legand_list), 'power_values': json.dumps(power_values)}
        print(context)
        return JsonResponse(context, safe=False)


# error test response
def my_test_500_view(request):
    # Return an "Internal Server Error" 500 response code.
    return HttpResponse(status=500)
