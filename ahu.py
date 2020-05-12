from util import *
import config


# The propose is to create a new Air handling unit and connect the specific zone into it
class AHU:
    def start(self, buildingpath):
        self.new_ahu = input("please name the new ahu: ")
        self.connect_zone = input("Specify the zone to connect with :")
        # Connecting to the IDA ICE API.
        pid = start()  # util.start() function
        test = ida_lib.connect_to_ida(b"5945", pid.encode())
        # Open a saved building
        self.building = call_ida_api_function(ida_lib.openDocument, buildingpath)

    # Find a reference AHU and make a copy with a new name
    def cloneAHU(self):
        ref_ahu = call_ida_api_function(ida_lib.getChildrenOfType, self.building, b"AHU")  # reference AHU
        cloned_ahu = call_ida_api_function(ida_lib.copyObject, ref_ahu[0]['value'],
                                           self.new_ahu_name.encode())  # a new copied AHU
        return cloned_ahu

    # Make connection to the required zone
    def modifyConn(self):
        result = self.cloneAHU(self.building, self.new_ahu)
        if not result:
            print("The clone action is unsuccessful with some problems")
        else:
            zone1 = ida_get_named_child(self.building, self.connect_zone)  # requied zone
            # Find existing AHU and make a new connection
            central_ahu = ida_get_named_child(zone1, "CENTRAL-AHU")
            chose_ahu = ida_get_named_child(central_ahu, "CHOSE_AHU")
            chose_ahu_val = ida_get_value(chose_ahu)  # AHU before modification
            print(type(chose_ahu_val))
            print("The choose ahu value before modification is " + chose_ahu_val)
            new_ahu = "\"" + self.new_ahu + "\""
            text_to_send = "{\"type\":\"string\",\"value\":" + new_ahu + "}"
            res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", chose_ahu, text_to_send.encode())
            chose_ahu_val_2 = ida_get_value(chose_ahu)
            print("choose ahu value is " + chose_ahu_val_2)

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = ida_lib.ida_disconnect()




#Unit Test
class TestAHU:
    def Test1(self):
        building_path = config.BUILDING_PATH
        ahu = AHU()
        ahu.start(building_path)


if __name__ == "__main__":
    testAHU = TestAHU()
    testAHU.Test1()
