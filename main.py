#before starting the connection, you need to go to "serivce.msc" to turn on IDAManagementService
from util import *


def main():
    # Connecting to the IDA ICE API.

    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")
    print("the building is %d" %building )

    nodes = call_ida_api_function(ida_lib.childNodes, building)
    print("How many child nodes: " + str(len(nodes)))
    for node in nodes:
        print("The node %s is %s \n" %(node['value'],ida_get_name(node['value'])))

    # zone1 = ida_get_named_child(building, "Zone 1")
    # central_ahu = ida_get_named_child(zone1, "CENTRAL-AHU")
    # nodes = call_ida_api_function(ida_lib.childNodes, central_ahu)
    # for node in nodes:
    #      print("The node %s is %s " %(node['value'],ida_get_name(node['value'])))

    end = ida_lib.ida_disconnect()


if __name__ == "__main__":
    main()