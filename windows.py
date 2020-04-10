from util import *


#show info of windows, walls, zones.
# Script functions


def findWall(building):
    zones = call_ida_api_function(ida_lib.getChildrenOfType, building, b"ZONE")
    for zone in zones:
        zone_name = ida_get_name(zone['value'])
        print(str(zone_name))
    zone2 = ida_get_named_child(building,"Zone")
    print("Zone 2 is "+str(zone2))
    if zone2 == False:
        print("Wrong name of zone")
        return False
    else:
        wall2 = ida_get_named_child(zone2, "WALL_2")
        if wall2 == False:
            print("Wrong name of Wall")
            return False
        else:
            return wall2
    return False

def cloneWindow(building):
    wall2 = findWall(building)
    if wall2 == False:
        print("clone is unsuccessful due to missing wall")
    else:

        ref_windows = call_ida_api_function(ida_lib.getWindows,building)
        # cloned_Window = call_ida_api_function(ida_lib.copyObject, ref_windows[0]['value'], b"Window added2")
        parent = call_ida_api_function(ida_lib.parentNode, cloned_Window)
        name_parent = ida_get_name(parent)
        print("the name of previous parent is "+str(name_parent))
        call_ida_api_function(ida_lib.removeChild, cloned_Window, parent)

        # new_parent = call_ida_api_function(ida_lib.setParentNode, ref_windows[0]['value'], wall2)
        # print("the new parent is "+str(ida_get_name(new_parent)))


        # newChildren = call_ida_api_function(ida_lib.appendChild, ref_windows[0]['value'], wall2)

        # for node in newChildren:
        #     print("The node %s is %s " % (node['value'], ida_get_name(node['value'])))
    # firstWindow = call_ida_api_function(ida_lib.copyObject, windows[0]['value'],b"Window 11")


    # call_ida_api_function(ida_lib.setParentNode, new_window, wall2)



def main():
    # Connecting to the IDA ICE API.

    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")

    cloneWindow(building)

    end = ida_lib.ida_disconnect()

if __name__ == "__main__":
    main()





