from util import *
import basic
import config
"""
    Solution to generate multiple zones for higher floors : clone existing zone and change its ceiling height
    Requirement: zones at the ground floor
    1. clone existing zones at the ground floor 
    2. change ceiling height of zones
    3. extend ceiling height of the building
    
    Question: can I create a new zone object directly by assigning its corners,height and so on ? 
"""

class floorOperation:
    def __init__(self, nf, fh):
        # Get user input for floors and ceiling height
        self.nf = nf
        self.fh = fh
        self.bh = nf * fh    #Total building height



    def changeCeilingHeight(self,val):
        print("Changing ceiling height of zones")
        origin_geometry = ida_get_named_child(val['value'], "GEOMETRY")
        ceiling = basic.showSingleChild(origin_geometry, "CEILING-HEIGHT")
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
        results = []
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
                    print(res_h_l)
                    results.append(res_h_l)

        for ele in results:
            if ele == False:
                return False
            else:
                return True

    def expandHeight(self,building):
        building_body = ida_get_named_child(building, "Building body")
        # showChildrenList(building_body)
        building_height = basic.showSingleChild(building_body, "HEIGHT")

        text_to_send = "{\"type\":\"number\",\"value\":" +"{0:.0f}".format(self.bh) + "}"
        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", building_height, text_to_send.encode())
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
    building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH)
    results =[]
    addFloor = floorOperation(nf,fh)
    if addFloor == False:
        end = ida_lib.ida_disconnect()
        results.append('Missing values for floor operation')
        return results
    if addFloor.expandHeight(building):
        res = addFloor.cloneZone(building)
        if res ==True:
            results.append('clone zone successfully')


    end = ida_lib.ida_disconnect()
    results.append('Something wrong')
    return results

if __name__ == "__main__":
    main(nf=3,fh=4)


