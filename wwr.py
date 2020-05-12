from basic import *
import math
import runscript

class WWR:

    def wwr1(self, building, wwr_val, wall_width_list, _ceiling_ht):
        """
         The first method to change wwr ratio is via API functions
        :param building: object
        :param wwr_val: wwr ratio value, e.g. 0.1 0.15 0.2 0.25 0.3 0.4
        :param wall_width_list
        :param _ceiling_ht
        :return:
        """
        # wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
        #                    13.899, 11.15, 9.98]
        # _ceiling_ht = 3
        # wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
        # building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        for zone in zones:
            zone_val = zone['value']
            walls = call_ida_api_function(ida_lib.getChildrenOfType, zone_val, b"WALL")
            for i in range(len(walls)):
                wall_val = walls[i]['value']
                # wins = call_ida_api_function(ida_lib.getWindows, wall_val)
                wins = call_ida_api_function(ida_lib.getChildrenOfType, wall_val, b"WINDOW")

                # Calculate X,Y,DX,DY
                sqrt_wwr = math.sqrt(wwr_val)
                win_wd = wall_width_list[i] * sqrt_wwr
                win_ht = _ceiling_ht*sqrt_wwr
                win_x = wall_width_list[i]/2 - win_wd/2
                win_y = _ceiling_ht/2 - win_ht/2
                newsize ={'X': win_x, 'Y': win_y, 'DX': win_wd, 'DY': win_ht}
                if type(wins) is list:
                    for win in wins:
                        win_val = win['value']
                        self.resizeWindow(win_val,newsize)            # Set attributes for windows


    def resizeWindow(self, win_obj, newsize):
        x = ida_get_named_child(win_obj, "X")
        x_val = ida_get_value(x)
        y = ida_get_named_child(win_obj, "Y")
        y_val = ida_get_value(y)
        dx = ida_get_named_child(win_obj, "DX")
        dx_val = ida_get_value(dx)
        dy = ida_get_named_child(win_obj, "DY")
        dy_val = ida_get_value(dy)
        print('value X', x_val,'; value Y', y_val, '; value DX', dx_val, '; value DY', dy_val)

        new_x = newsize['X']
        new_y = newsize['Y']
        new_dx = newsize['DX']
        new_dy = newsize['DY']

        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_dx) + "}"
        res_dx = call_ida_api_function(ida_lib.setAttribute, b"VALUE", dx, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_dy) + "}"
        res_dy = call_ida_api_function(ida_lib.setAttribute, b"VALUE", dy, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_y) + "}"
        res_y = call_ida_api_function(ida_lib.setAttribute, b"VALUE", y, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.2f}".format(new_x) + "}"
        res_x = call_ida_api_function(ida_lib.setAttribute, b"VALUE", x, text_to_send.encode())

        print(res_dx, res_dy, res_x, res_y)



    def wwr2(self, building, wwr_val, wall_width_list, _ceiling_ht, folder, idm_name):
        """
         The second method is to use the Lisp scripting method to change wwr ratio values.
         The speed is fast and easy to use
        :param building:
        :param wwr_val:
        :param wall_width_list:
        :param _ceiling_ht:
        :return:
        """

        wins = []
        doors = []
        for i in range(len(wall_width_list)):
            wall_name = 'WALL_'+str(i+1)
            # Calculte win_x, _y, _dx, _dy
            sqrt_wwr = math.sqrt(wwr_val)
            win_wd = wall_width_list[i] * sqrt_wwr
            win_ht = _ceiling_ht * sqrt_wwr
            win_x = wall_width_list[i] / 2 - win_wd / 2
            win_y = _ceiling_ht / 2 - win_ht / 2
            newsize = {'wall_name': wall_name, 'win_x': win_x, 'win_y': win_y, 'win_dx': win_wd, 'win_dy': win_ht}
            wins.append(newsize)

        # building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        runScript = runscript.RunScript()
        generated = runScript.generate_script(wins,doors,5, False)
        res = runScript.apply_script(building, generated)

        # Save the new idm file
        # path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' +wwr_val + '.idm'
        path = folder + idm_name + '_wwr' + str(wwr_val) + '.idm'
        saveIDM(building, path)
        time.sleep(1)

        return building

    # Add new windows according to WWR
    def wwr2_new(self, building, wwr_val, wall_width_list, _ceiling_ht, folder, idm_name, new =True):
        """
         The second method is to use the Lisp scripting method to change wwr ratio values.
         The speed is fast and easy to use
        :param building:
        :param wwr_val:
        :param wall_width_list:
        :param _ceiling_ht:
        :param new: if add new windows(True) or modify windows
        :return:
        """

        wins = []
        doors = []
        for i in range(len(wall_width_list)):
            wall_name = 'WALL_'+str(i+1)
            # Calculte win_x, _y, _dx, _dy
            sqrt_wwr = math.sqrt(wwr_val)
            win_wd = wall_width_list[i] * sqrt_wwr
            win_ht = _ceiling_ht * sqrt_wwr
            win_x = wall_width_list[i] / 2 - win_wd / 2
            win_y = _ceiling_ht / 2 - win_ht / 2
            newsize = {'wall_name': wall_name, 'win_x': win_x, 'win_y': win_y, 'win_dx': win_wd, 'win_dy': win_ht}
            wins.append(newsize)

        # building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        runScript = runscript.RunScript()
        generated = runScript.generate_script(wins,doors,len(zones), new)
        res = runScript.apply_script(building, generated)

        # Save the new idm file
        # path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' +wwr_val + '.idm'
        path = folder + idm_name + '_wwr' + str(wwr_val) + '.idm'
        saveIDM(building, path)
        time.sleep(2)

        return building







class TestWWR:
    def testWWR_md1(self):
        wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                          13.899, 11.15, 9.98]
        _ceiling_ht = 3
        wwrs = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
        wwrPro = WWR()
        for wwr in wwrs:
            building = connectIDA()
            wwrPro.wwr1(building, wwr, wall_width_list, _ceiling_ht)


    def testWWR_md2(self):
        wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                          13.899, 11.15, 9.98]
        _ceiling_ht = 3
        wwrs = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]

        folder = 'd:\\ide_mine\\changing\\'
        base_idm = 'ut1_7floorwithWin'
        building_path = folder + base_idm + '.idm'


        wwrPro = WWR()
        for wwr in wwrs:
            building = connectIDA2(building_path)
            wwrPro.wwr2(building, wwr, wall_width_list, _ceiling_ht, folder, base_idm)





if __name__ == "__main__":
    test1 = TestWWR()
    test1.testWWR_md2()