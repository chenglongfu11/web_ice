from util import *
from webproject.webapplication import config


def cloneAHU(building, new_ahu_name):
    ref_ahu = call_ida_api_function(ida_lib.getChildrenOfType, building, b"AHU")
    cloned_ahu = call_ida_api_function(ida_lib.copyObject, ref_ahu[0]['value'], new_ahu_name.encode())
    return cloned_ahu

def modifyConn(building, new_ahu, connect_zone):
    result = cloneAHU(building, new_ahu)
    if result == False:
        print("The clone action is unsuccessful with some problems")
    else:

            zone1 = ida_get_named_child(building, connect_zone)
            central_ahu = ida_get_named_child(zone1, "CENTRAL-AHU")
            chose_ahu = ida_get_named_child(central_ahu, "CHOSE_AHU")
            chose_ahu_val = ida_get_value(chose_ahu)
            print(type(chose_ahu_val))
            print("The choose ahu value before modifitication is " + chose_ahu_val)
            new_ahu = "\"" + new_ahu + "\""
            text_to_send = "{\"type\":\"string\",\"value\":" + new_ahu + "}"
            res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", chose_ahu, text_to_send.encode())
            chose_ahu_val_2 = ida_get_value(chose_ahu)
            print("choose ahu value is " + chose_ahu_val_2)





def main():
    print("the propose is to create a new Air handling unit and connect the specific zone into it")
    new_ahu = input("please name the new ahu: ")
    connect_zone = input("Specify the zone to connect with :")
    # Connecting to the IDA ICE API.
    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH)

    modifyConn(building, new_ahu, connect_zone)

    end = ida_lib.ida_disconnect()

if __name__ == "__main__":
    main()