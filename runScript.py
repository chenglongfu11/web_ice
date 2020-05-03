from util import *
import config
from zone_strcs import win_strc, therm_bdg, door_strc
import zone_clone
from zone_strcs import zone_strc
from basic import *


class RunScript:

    def apply_script(self, building, script):
        res = call_ida_api_function(ida_lib.runIDAScript, building, script.encode())
        print(res)
        return res

    # Aggregated scripting generator    wins each floor, doors each floor
    def generate_script(self, wins, doors, num_zone=1):
        scriptList = []
        heading, endnote = self.script_bsc()
        scriptList.append(heading)

        for i in range(num_zone):
            zone_name = 'Zone ' + str(i + 1)
            zoneScrip = zone_strc.zone_strc(wins, doors, zone_name)
            scriptList.append(zoneScrip)

        scriptList.append(endnote)
        ressss = ' '.join(scriptList)
        print(ressss)
        return ressss

    def script_bsc(self):
        script_heading = '(:UPDATE [@] '
        script_endnote = ')'
        return script_heading, script_endnote

    # """subfunction
    #         ( (CE-ZONE :N "Zone 1")
    #
    #         )"""
    # def zoneScriptTitle(self, zone_name11):
    #     zone_1 = '((CE-ZONE :N "' + zone_name11 + '")'
    #     zone_2 = ')'
    #     return zone_1, zone_2
    #
    #
    # #Zone based scripting, windows and doors
    # def zoneScript(self, wins, doors, zone_name = 'Zone 1'):
    #     scriptList = []
    #     zone_name1 = zone_name
    #
    #     zoneSc_1, zoneSc_2 = self.zoneScriptTitle(zone_name1)
    #     scriptList.append(zoneSc_1)
    #
    #     #thermal bridge script
    #     win_num = len(wins)
    #     door_num = len(doors)
    #     tbrigeSc = therm_bdg.thermalbridgeScript(win_num, door_num)
    #     scriptList.append(tbrigeSc)
    #
    #     winScList = []
    #     #windows script
    #     for win in wins:
    #         win_dx = '2'
    #         win_dy = '1'
    #         detailed = 0
    #         glazing = 0
    #         # win_x  win_y
    #         if 'win_dx' in win.keys():
    #             win_dx = win['win_dx']
    #         if 'win_dy' in win.keys():
    #             win_dy = win['win_dy']
    #         if 'detailed' in win.keys():
    #             detailed = win['detailed']
    #         if 'glazing' in win.keys():
    #             glazing = win['glazing']
    #
    #         winSc = win_strc.windowScript(win['w_wall_name'], win['win_x'], win['win_y'], detailed, win_dx, win_dy, glazing)
    #
    #         winScList.append(winSc)
    #         # windowScript(self, wall_name, win_x, win_y, detailed_win=False, win_dx='2', win_dy='1', glazing=0):
    #
    #     doorScList = []
    #     for door in doors:
    #         door_y = '0'
    #         door_dx = '0.8'
    #         door_dy = '2'
    #         if 'door_y' in door.keys():
    #             door_y = door['door_y']
    #         if 'door_dx' in door.keys():
    #             door_dx = door['door_dx']
    #         if 'door_dy' in door.keys():
    #             door_dy = door['door_dy']
    #
    #         doorSc = door_strc.openingScript(door['d_wall_name'], door['door_x'], door_y, door_dx, door_dy)
    #         doorScList.append(doorSc)
    #
    #     scriptList.append(' '.join(winScList))
    #     scriptList.append(' '.join(doorScList))
    #     scriptList.append(zoneSc_2)
    #     re = ''.join(scriptList)
    #
    #     print(re)
    #     return re


# Unit test
class TestRunScript:

    def testScriptGene(self, ceiling_ht, wall_width):
        _run = RunScript()

        # allocate doors' parameters
        doors = []
        door = {}
        door['d_wall_name'] = 'WALL_6'
        door['door_x'] = '3.21'
        doors.append(door)

        # allocate wins' parameters, on each wall with proper size, add a window
        wins = []
        win_dx = 1.5
        win_dy = 1.2
        for i in range(len(wall_width)):
            width = wall_width[i]
            if width > win_dx + 2 and ceiling_ht > win_dy:  # to make sure it is in the zone
                win = {}
                win['w_wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        generated = _run.generate_script(wins, doors)
        print(generated)

    def testZoneCloneAND_DW(self, ceiling_ht, wall_width):
        _run = RunScript()
        zoneClone = zone_clone.ZoneClone()

        # Clone zones
        building = connectIDA()
        nfloor = zoneClone.clone_zones_pro(building, ceiling_ht, "Floor_36")
        nfloor = int(nfloor)

        # Add components to zones
        wall_height = ceiling_ht
        # wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554, 13.899, 11.15, 9.98]
        doors = []
        door = {}
        door['d_wall_name'] = 'WALL_6'
        door['door_x'] = '3.21'
        doors.append(door)

        wins = []
        win_dx = 1.5
        win_dy = 1.2
        for i in range(len(wall_width)):
            width = wall_width[i]
            if width > win_dx + 2 and wall_height > win_dy:  # to make sure it is in the zone
                win = {}
                win['w_wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        win2 = {}
        win2['w_wall_name'] = 'WALL_13'
        win2['win_x'] = '26.015'
        win2['win_y'] = '0.8'
        win2['win_dx'] = '3'
        win2['win_dy'] = '1.8'
        win2['detailed'] = 1  # true 1   false 0
        win2['glazing'] = 1
        wins.append(win2)

        sc = _run.generate_script(wins, doors, nfloor)
        _run.apply_script(building, sc)



    def test_window2(self, ceiling_height):
        wall_height = ceiling_height
        wall_width = [11.63]
        wins = []
        doors = []
        win_dx = 1.5
        win_dy = 1.2

        for i in range(len(wall_width)):
            width = wall_width[i]
            if width > win_dx + 2 and wall_height > win_dy:  # to make sure it is in the zone
                win = {}
                win['w_wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        run1 = RunScript()
        nfloor = 7
        sc = run1.generate_script(wins, doors, nfloor)


    def testApplyScript(self, ceiling_height, wall_width_list):
        wall_height = ceiling_height
        doors = []
        door = {}
        door['d_wall_name'] = 'WALL_6'
        door['door_x'] = '3.21'
        doors.append(door)

        wins = []
        win_dx = 1.5
        win_dy = 1.2
        for i in range(len(wall_width_list)):
            width = wall_width_list[i]
            if width > win_dx + 2 and wall_height > win_dy:  # to make sure it is in the zone
                win = {}
                win['w_wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        win2 = {}
        win2['w_wall_name'] = 'WALL_13'
        win2['win_x'] = '26.015'
        win2['win_y'] = '0.8'
        win2['win_dx'] = '3'
        win2['win_dy'] = '1.8'
        win2['detailed'] = 1  # true 1   false 0
        win2['glazing'] = 1
        wins.append(win2)

        run1 = RunScript()
        sc = run1.generate_script(wins, doors)
        building = connectIDA()
        run1.apply_script(building, sc)
        # run1.saveIDM("D:\\ide_mine\\changing\\ut1_3.idm",1)


if __name__ == "__main__":
    wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                       13.899, 11.15, 9.98]
    _ceiling_ht = 3

    _test = TestRunScript()
    # test1.sw1_dw1_d1(2.6)
    _test.testZoneCloneAND_DW(_ceiling_ht, wall_width_list)
    # test1.windowtwo(3)
    # _test.testScriptGene(_ceiling_ht, wall_width_list)
