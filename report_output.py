import re
import sys
import traceback

import showList
from dbhelper import DB
from util import *


class Report_out():
    def __init__(self):
        try:
            # connect to database
            self.db = DB(database="energy_report_consumption")

            # Connecting to the IDA ICE API.
            pid = start()
            test = ida_lib.connect_to_ida(b"5945", pid.encode())
            # connect to ida ice document
            self.building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\building_work1.idm")
            self.building_name = ida_get_name(self.building)
            self.energy_report = showList.showSingleChild(self.building, 'ENERGY-REPORT')
            self.standard_report_list = ['Lighting, facility', 'Electric cooling', 'HVAC aux',
                                         'Fuel heating', 'Domestic hot water', 'Equipment, tenant']
        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.end = ida_lib.ida_disconnect()
        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    # Insert building information into db, can be extended
    def building_repo(self):
        if self.building_name:
            self.bid = self.db.insertBuil(self.building_name)
        if self.bid:
            print("bid got")
            return True

    # Insert simulation information into db, sid, bid, simulation-option, datetime
    def simulation_repo(self, simulation_option="change some parameter"):
        self.sid = self.db.insertSimu(self.bid, simulation_option)
        if self.sid:
            return True

    # Insert consumption_report into db
    def consumption_report(self):
        try:
            consumption = showList.showSingleChild(self.energy_report, 'CONSUMPTION')
            value_list = showList.showChildrenListValue(consumption)
            consumption_dict = {}
            check =1
            consumption_table_name = {
                'Lighting, facility': 'consump_lighting_facility', 'Electric cooling': 'consump_electric_cooling',
                'HVAC aux': 'consump_hvac', 'Fuel heating': 'consump_fuel_heating',
                'Domestic hot water': 'consump_domestic_hot_water', 'Equipment, tenant': 'consump_equipment_tenant'}

            # Extract key and values from consumption
            for key, val in value_list.items():
                consumption_dict[key] = re.findall(r"\d+\.?\d*", val)

            for key, val in consumption_dict.items():
                print(key + '==')

            for i in range(len(self.standard_report_list)):
                if self.standard_report_list[i] in consumption_dict:
                    table_name = consumption_table_name.get(self.standard_report_list[i])
                    self.db.insertEle(check,self.sid, self.bid, consumption_dict.get(self.standard_report_list[i]),
                                      table_name)
                else:
                    print('Unsuccessfully inserting ' + self.standard_report_list[
                        i] + ' data into energy report- consumption')

        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    def peak_power_report(self):
        try:
            demand = showList.showSingleChild(self.energy_report, 'DEMAND')
            value_list = showList.showChildrenListValue(demand)
            peak_power_dict = {}
            check =2
            pk_power_table_name = {'Lighting, facility': 'pk_power_lighting_facility',
                                   'Electric cooling': 'pk_power_electric_cooling',
                                   'HVAC aux': 'pk_power_hvac', 'Fuel heating': 'pk_power_fuel_heating',
                                   'Domestic hot water': 'pk_power_domestic_hot_water',
                                   'Equipment, tenant': 'pk_power_equipment_tenant'}
            # Extract key and values from peak power
            for key, val in value_list.items():
                peak_power_dict[key] = re.findall(r"\d+\.?\d*", val)

            for key, val in peak_power_dict.items():
                print(key + '==')

            for i in range(len(self.standard_report_list)):
                if self.standard_report_list[i] in peak_power_dict:
                    table_name = pk_power_table_name.get(self.standard_report_list[i])
                    self.db.insertEle(check, self.sid, self.bid, peak_power_dict.get(self.standard_report_list[i]), table_name)
                else:
                    print('Unsuccessfully inserting ' + self.standard_report_list
                    [i] + 'data into energy report- peak power')

        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)


# unit test
class TestReportOutput():
    def __init__(self):
        self.report_out = Report_out()

    # consumption report test
    def testConsumptionReport(self):
        try:
            self.report_out.building_repo()
            self.report_out.simulation_repo("Window width = 2m +")
            self.report_out.consumption_report()
            self.report_out.peak_power_report()
        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)

    # peak power report test
    def testPeakPowerReport(self):
        try:
            self.report_out.building_repo()
            self.report_out.simulation_repo("Window width = 2m +")
            self.report_out.peak_power_report()
        except:
            print("Exception in user code:")
            print('-' * 60)
            traceback.print_exc(file=sys.stdout)
            print('-' * 60)


if __name__ == "__main__":
    tr = TestReportOutput()
    tr.testConsumptionReport()
    # tr.testPeakPowerReport()