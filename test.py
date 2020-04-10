from util import *
import run_simu

test = ida_lib.connect_to_ida(b"5945", pid.encode())
# Open a saved building
building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")
building_2 = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building2.idm")
print("the building is %d" % building)
print(type(building))
print(str(ida_get_name(building)))
print("the building is %d" % building_2)
print(str(ida_get_name(building_2)))
run_simu.do_simulation(building)
energy_report = ida_get_named_child(building, "ENERGY-REPORT")
rep_res = call_ida_api_function(ida_lib.printReport, energy_report, b"d:\\ide_mine\\1.pdf", 2)
print("Printing report {}".format(rep_res))


run_simu.do_simulation(building_2)
energy_report_2 = ida_get_named_child(building_2, "ENERGY-REPORT")
rep_res_2 = call_ida_api_function(ida_lib.printReport, energy_report_2, b"d:\\ide_mine\\2.pdf", 2)
print("Printing report {}".format(rep_res_2))

text_to_send = "[{\"type\":\"object\",\"value\":1},{\"type\":\"object\",\"value\":2}]"
# text_to_send = "[{\"type\":\"test_building3\",\"value\":1" + "{0:.0f}".format(
#     1) + "},{\"type\":\"test_building2\",\"value\":" + "{0:.0f}".format(1) + "}]"
res_h_l = call_ida_api_function(ida_lib.compareResults, text_to_send.encode(), b"d:\\ide_mine\\3.pdf", 2)