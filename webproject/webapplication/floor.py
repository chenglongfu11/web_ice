from .utils import *
from . import showList


class floorOperation:
    def __init__(self, nf, fh):
        # Get user input for floors and ceiling height
        self.nf = int(nf)
        self.fh = float(fh)
        self.bh = nf * fh    #Total building height



    def changeCeilingHeight(self,val):
        print("Changing ceiling height of zones")
        origin_geometry = ida_get_named_child(val['value'], "GEOMETRY")
        ceiling = showList.showSingleChild(origin_geometry, "CEILING-HEIGHT")
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(self.fh) + "}"
        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", ceiling, text_to_send.encode())
        ress = ida_get_value(ceiling)
        if ress == self.fh:
            return True
        else:
            print("Fail to change ceiling height")
            return False




    def cloneZone(self,building):
        zones = call_ida_api_function(ida_lib.getChildrenOfType, building, b"ZONE")
        fail_results = 0
        for i, val in enumerate(zones):
            if self.changeCeilingHeight(val):

                for j in range(self.nf-1):
                    zone_name = "Zone added"+str(i)+str(j)
                    cloned_zone = call_ida_api_function(ida_lib.copyObject, val['value'], zone_name.encode())
                    geometry = ida_get_named_child(cloned_zone, "GEOMETRY")
                    floor_height = ida_get_named_child(geometry, "FLOOR_HEIGHT_FROM_GROUND")
                    # print(str(floor_height))
                    fl_val = ida_get_value(floor_height)
                    # print("the current floor height is " + str(fl_val))
                    text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(self.fh*(j+1)) + "}"
                    res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", floor_height, text_to_send.encode())
                    # return value from call_ida_api_function is True or False
                    if res_h_l == False:
                        print('Clong zone unsuccessfully' )
                        fail_results = fail_results+1

        if fail_results == 0:
            return True
        else:
            return False


    def expandHeight(self,building):
        building_body = ida_get_named_child(building, "Building body")
        # showChildrenList(building_body)
        building_height = showList.showSingleChild(building_body, "HEIGHT")

        text_to_send = "{\"type\":\"number\",\"value\":" +"{0:.0f}".format(self.bh) + "}"

        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", building_height, text_to_send.encode())
        #return value from call_ida_api_function is True or False
        ress = ida_get_value(building_height)
        if ress == self.bh:
            print("Succefully changed building height to  %s" %building_height)
            return True
        else:
            print("Error in changing building height")
            return False



def main(nf,fh):

    pid = start()
    # Connecting to the IDA ICE API.
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")
    results =[]
    addFloor = floorOperation(nf,fh)

    if addFloor.expandHeight(building):
        res = addFloor.cloneZone(building)
        if res:
            results.append('clone zone successfully')

    end = ida_lib.ida_disconnect()
    return results

