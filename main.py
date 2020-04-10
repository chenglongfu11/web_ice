#before starting the connection, you need to go to "serivce.msc" to turn on IDAManagementService
from util import *

def showChildrenList(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    for child in children:
        name = ida_get_name(child['value'])
        print("The %s is %s" %(child['value'], name))


def showChildrenListValue(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    for child in children:
        name = ida_get_name(child['value'])
        value = ida_get_value(child['value'])
        print("The %s is %s" %(name, value))

def showSingleChild(parent, child_name):
    element = ida_get_named_child(parent, child_name)
    element_val = ida_get_value(element)
    print("The current %s value is %d, and the type is %s" %(child_name,element_val,type(element_val)))


def main():
    # Connecting to the IDA ICE API.

    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")
    print("the building is %d" %building )

    building_body = ida_get_named_child(building, "Building body")
    # showChildrenList(building_body)
    showSingleChild(building_body, "HEIGHT")
    # height = ida_get_named_child(building_body, "Roof")
    # bottom = ida_get_named_child(building_body, "BOTTOM")
    # height_val = ida_get_value(height)
    # bottom_val = ida_get_value(bottom)
    # print("The current height value is %d" %height)
    # print("the type is "+str(type(height_val)))
    # print("The current bottom value is %d" %bottom_val)
    # print("the type is "+str(type(height_val)))
    # text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(-10) + "}"
    # res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", bottom, text_to_send.encode())
    # print(str(res_h_l))
    if building_body != False:
        print("wrong input")
    else:

        nodes = call_ida_api_function(ida_lib.childNodes, building_body)
        print("How many child nodes: " + str(len(nodes)))
        for node in nodes:
            print("The node %s is %s " %(node['value'],ida_get_name(node['value'])))

    # zone1 = ida_get_named_child(building, "Zone 1")
    # central_ahu = ida_get_named_child(zone1, "CENTRAL-AHU")
    # nodes = call_ida_api_function(ida_lib.childNodes, central_ahu)
    # for node in nodes:
    #      print("The node %s is %s " %(node['value'],ida_get_name(node['value'])))

    end = ida_lib.ida_disconnect()


if __name__ == "__main__":
    main()