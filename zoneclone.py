from util import *
import basic
from basic import *

"""
    Solution to generate multiple zones for higher floors : clone existing zone and change its ceiling height
    Requirement: zones at the ground floor
    1. clone existing zones at the ground floor 
    2. change ceiling height of zones
    3. extend ceiling height of the building
    
    Question: can I create a new zone object directly by assigning its corners,height and so on ? 
"""


class ZoneClone:

    def edit_ceiling_ht(self, val, ceiling_ht):
        """
        :param val: zone object
        :param ceiling_ht: target ceiling height
        :return: success or fail
        """

        print("Changing ceiling height")
        origin_geometry = ida_get_named_child(val['value'], "GEOMETRY")  # geometry object
        ceiling = basic.showSingleChild(origin_geometry, "CEILING-HEIGHT")  # ceiling height object

        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(ceiling_ht) + "}"  # float(ceiling_ht)
        res_1 = call_ida_api_function(ida_lib.setAttribute, b"VALUE", ceiling, text_to_send.encode())

        # Check the current ceiling height
        ress = ida_get_value(ceiling)
        if ress == ceiling_ht:
            return True
        else:
            name = ida_get_name(val['value'])
            print("Fail to change ceiling height for %s" % name)
            return False



    def clone_zone(self, building, ceiling_ht, num_floor):
        """
        Clone zone: known building, ceiling_ht, num_floor, we can clone zones
        :param building: object
        :param ceiling_ht:
        :param num_floor:
        :return:
        """
        zones = call_ida_api_function(ida_lib.getChildrenOfType, building, b"ZONE")
        results = []
        new_file_name = ''

        # Single zone on each floor
        if len(zones) == 1:

            val = zones[0]
            if self.edit_ceiling_ht(val, ceiling_ht):  # Edit the ceiling ht of the base zone
                for j in range(num_floor - 1):
                    zone_name = "Zone " + str(j + 2)
                    cloned_zone = call_ida_api_function(ida_lib.copyObject, val['value'],
                                                        zone_name.encode())  # Clone the zone object

                    # Edit the geometry of the cloned zone
                    geometry = ida_get_named_child(cloned_zone, "GEOMETRY")
                    floor_ht_fr = ida_get_named_child(geometry, "FLOOR_HEIGHT_FROM_GROUND")
                    fl_val = ida_get_value(floor_ht_fr)  # Original floor height from ground
                    # Algorithm: floor height from ground = ceiling ht * floor
                    # e.g floor 1: 0m; floor 3: ceiling_ht*2 m
                    text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(ceiling_ht * (j + 1)) + "}"
                    res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", floor_ht_fr, text_to_send.encode())
                    print(res_h_l)
                    results.append(res_h_l)
                    new_file_name = ida_get_name(building) + '_' + str(num_floor) + 'floor'

        else:
            for i, val in enumerate(zones):
                if self.edit_ceiling_ht(val):

                    for j in range(num_floor - 1):
                        zone_name = "Zone added" + str(i) + str(j)
                        cloned_zone = call_ida_api_function(ida_lib.copyObject, val['value'], zone_name.encode())
                        geometry = ida_get_named_child(cloned_zone, "GEOMETRY")
                        floor_height = ida_get_named_child(geometry, "FLOOR_HEIGHT_FROM_GROUND")
                        # print(str(floor_height))

                        fl_val = ida_get_value(floor_height)
                        # print("the current floor height is " + str(fl_val))

                        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(ceiling_ht * (j + 1)) + "}"
                        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", floor_height,
                                                        text_to_send.encode())
                        print(res_h_l)
                        results.append(res_h_l)
                        new_file_name = ida_get_name(building) + '_' + str(num_floor) + 'floor'

        # Check results
        for ele in results:
            if not ele:
                return False, new_file_name
            else:
                return True, new_file_name


    # Edit building height
    def edit_bld_ht(self, building, height, body_name="Floor_36"):
        """
         Edit building height
        :param building: object
        :param height: target building height
        :param body_name: Building_body  Floor_36  难以确定，需要用户检查
        :return:

        """

        building_body = ida_get_named_child(building, body_name)  # building body object
        # showChildrenList(building_body)
        building_height = basic.showSingleChild(building_body, "HEIGHT")  # building body height object

        # Set building height attribute
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.0f}".format(height) + "}"
        res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", building_height, text_to_send.encode())

        # Check the current building height
        ress = ida_get_value(building_height)
        if ress == height:
            print("Successfully changed building height to  %s" % building_height)
            return True
        else:
            print("Error in changing building height")
            return False

    # Building current height
    def bld_cur_ht(self, building, body_name="Floor_36"):
        building_body = ida_get_named_child(building, body_name)  # Building body object
        bld_ht = basic.showSingleChild(building_body, "HEIGHT")  # building body height object
        bld_ht_val = ida_get_value(bld_ht)  # get value

        return bld_ht_val


    def clone_zones_pro(self, building, ceiling_ht, body_name="Floor_36"):
        """
        Algorithm: known building ht and ceiling ht of zone, calculate num of floors, clone zones
        :param building: object
        :param ceil_height:
        :param body_name:
        :return: number of floors
        """

        # Calculate num of floor
        cur_ht = self.bld_cur_ht(building, body_name)         # Get current height of the building
        num_floor = int(cur_ht / ceiling_ht)

        res = self.clone_zone(building, ceiling_ht, num_floor)
        print(res)
        return num_floor




# Unit test
class TestZoneClone:
    def testCloneBuilding(self, ceil_height, nfloor):
        zoneClone = ZoneClone()
        building_obj = connectIDA()
        res = zoneClone.clone_zone(building_obj, ceil_height, nfloor)
        print(res)

    def testCur_ht(self):
        zoneClone = ZoneClone()
        building_obj = connectIDA()
        res = zoneClone.bld_cur_ht(building_obj, "Floor_36")
        print(res, type(res))

    def testCloneBuilding2(self, ceil_height):
        zoneClone = ZoneClone()
        building_obj = connectIDA()

        # Calculate the num of floor
        existH = zoneClone.bld_cur_ht(building_obj, "Floor_36")
        nfloor = int(existH / ceil_height)
        res = zoneClone.clone_zone(building_obj, ceil_height, nfloor)
        print(res)

    def testCloneBuilding3(self, ceiling_ht):
        zoneClone = ZoneClone()
        building_obj = connectIDA()

        nfloor = zoneClone.clone_zones_pro(building_obj, ceiling_ht, "Floor_36")
        print(nfloor)


if __name__ == "__main__":
    testZoneClone = TestZoneClone()
    testZoneClone.testCloneBuilding(2.6,3)
    testZoneClone.testCur_ht()
    testZoneClone.testCloneBuilding2(3)
    testZoneClone.testCloneBuilding3(4)

# def main(nf,fh):
#
#     pid = start()
#     # Connecting to the IDA ICE API.
#     test = ida_lib.connect_to_ida(b"5945", pid.encode())
#     # Open a saved building
#     building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH)
#     results =[]
#     addFloor = floorOperation(nf,fh)
#     if addFloor == False:
#         end = ida_lib.ida_disconnect()
#         results.append('Missing values for floor operation')
#         return results
#     if addFloor.expandHeight(building):
#         res = addFloor.cloneZone(building)
#         if res ==True:
#             results.append('clone zone successfully')
#
#
#     end = ida_lib.ida_disconnect()
#     results.append('Something wrong')
#     return results
