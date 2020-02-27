from util import *


def cloneZone(building, fh=3):
    zones = call_ida_api_function(ida_lib.getChildrenOfType, building, b"ZONE")
    for i, val in enumerate(zones):
        zone_name = "Zone added"+str(i)
        cloned_zone = call_ida_api_function(ida_lib.copyObject, val['value'], zone_name.encode())
        geometry= ida_get_named_child(cloned_zone, "GEOMETRY")
        floor_height = ida_get_named_child(geometry, "FLOOR_HEIGHT_FROM_GROUND")
        print(str(floor_height))
        fl_val = ida_get_value(floor_height)
        print("the current floor height is "+ str(fl_val))
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(fh.__float__()) + "}"
        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", floor_height, text_to_send.encode())



def main():
    # Connecting to the IDA ICE API.
    fh = float(input('Please insert the new floor height :'))
    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")

    cloneZone(building, fh)

    end = ida_lib.ida_disconnect()

if __name__ == "__main__":
    main()
