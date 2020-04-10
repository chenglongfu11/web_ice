from util import *
from webproject.webapplication import config


# print(building)
def show_buildinginfo(building):
    name = ida_get_name(building)
    print("Opening case: " + name)

#现在存在的问题： Your License is not allowed for simulation
#如果存在error也会直接return回来
#Doing simulation
def do_simulation(building):
    print("Now performing simulation...")
    sim_res = call_ida_api_function(ida_lib.runSimulation, building, 1)
    print("the simulation result is " + str(sim_res))
    print("Simulation done...")




#Retrieving data
def data_retrieve(building):
    energy_report = ida_get_named_child(building,"ENERGY-REPORT")
    demand = ida_get_named_child(energy_report,"DEMAND")
    fuel_heating = ida_get_named_child(demand,"Fuel heating")
    fuel_heating_value = ida_get_value(fuel_heating)
    print("Fuel heating, peak demand: " + str(fuel_heating_value) + " kW")

#Disconnect

def disconnect():
    end = ida_lib.ida_disconnect()
    print("Finished")



def main():
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    print("the connect is " + str(test))
    building1 = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH)
    show_buildinginfo(building1)
    do_simulation(building1)
    data_retrieve(building1)
    disconnect()





if __name__ == "__main__":
    main()