# Unit test
import zoneclone
from basic import *
from runscript import RunScript
import pandas as pd
import numpy as np


class TestRunScript:

    def testScriptGene(self, ceiling_ht, wall_width):
        # allocate doors' parameters
        doors = []
        door = {}
        door['wall_name'] = 'WALL_6'
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
                win['wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        _run = RunScript()
        generated = _run.generate_script(wins, doors)
        print(generated)

    def testGene2(self):
        wins =[]
        win2 = {}
        win2['wall_name'] = 'WALL_13'
        win2['win_x'] = '26.015'
        win2['win_y'] = '0.8'
        win2['win_dx'] = '3'
        win2['win_dy'] = '1.8'
        win2['detailed'] = 1  # true 1   false 0
        win2['glazing'] = 1
        wins.append(win2)
        doors=[]

        _run = RunScript()
        generated = _run.generate_script(wins, doors)
        print(generated)



    def testZoneCloneAND_DW(self, ceiling_ht, wall_width):
        _run = RunScript()
        zoneClone = zoneclone.ZoneClone()

        # Clone zones
        building = connectIDA()
        nfloor = zoneClone.clone_zones_pro(building, ceiling_ht, "Floor_36")
        nfloor = int(nfloor)

        # Add components to zones
        wall_height = ceiling_ht
        # wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554, 13.899, 11.15, 9.98]
        doors = []
        door = {}
        door['wall_name'] = 'WALL_6'
        door['door_x'] = '3.21'
        doors.append(door)

        wins = []
        win_dx = 1.5
        win_dy = 1.2
        for i in range(len(wall_width)):
            width = wall_width[i]
            if width > win_dx + 2 and wall_height > win_dy:  # to make sure it is in the zone
                win = {}
                win['wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        win2 = {}
        win2['wall_name'] = 'WALL_13'
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
                win['wall_name'] = 'WALL_' + str(i + 1)
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
        door['wall_name'] = 'WALL_6'
        door['door_x'] = '3.21'
        doors.append(door)

        wins = []
        win_dx = 1.5
        win_dy = 1.2
        for i in range(len(wall_width_list)):
            width = wall_width_list[i]
            if width > win_dx + 2 and wall_height > win_dy:  # to make sure it is in the zone
                win = {}
                win['wall_name'] = 'WALL_' + str(i + 1)
                win['win_x'] = str(width / 2 - win_dx / 2)
                win['win_y'] = '0.8'
                win['win_dx'] = '1.5'
                win['win_dy'] = '1.2'
                wins.append(win)

        win2 = {}
        win2['wall_name'] = 'WALL_13'
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

    def testAdvWindow(self):
        # win: w_wall_name, win_x, win_y, win_dx, win_dy, detailed, glazing, shading, recess, schedule, material
        #                 schedule: plan_type, start, end
        #                 material: area_fraction, u_value
        schedules = {'plan_type': 4, 'start': 8, 'end': 17}
        materials = {'area_fraction': 0.5, 'u_value': 5}
        winx = {'wall_name': 'WALL_6', 'win_x': 3, 'win_y': 0.8, 'detailed': 1, 'glazing': 2, 'shading': 'YES',
               'recess': 2, 'schedule': schedules, 'material': materials}

        # Windows from CSV
        df = pd.read_csv('d:\\untitled\\buildings\\windows.csv')
        wins = df.to_dict(orient='records')
        for win in wins:
            win1 = win
            for key, val in win.copy().items():
                if pd.isnull(val):
                    win1.pop(key)
            win = win1
            win['schedule'] = schedules
            win['material'] = materials

        # Doors from CSV
        df2 = pd.read_csv('d:\\untitled\\buildings\\doors.csv')
        doors = df2.to_dict(orient='records')
        for door in doors:
            door1 = door
            for key, val in door.copy().items():
                if pd.isnull(val):
                    door1.pop(key)
            door = door1

        # doors = []
        # door = {}
        # door['wall_name'] = 'WALL_6'
        # door['door_x'] = '3.21'
        # doors.append(door)


        # Clone zones
        ceiling_ht = 3
        # zoneClone = zoneclone.ZoneClone()
        # building = connectIDA()
        # nfloor = zoneClone.clone_zones_pro(building, ceiling_ht, "Floor_36")
        # nfloor = int(nfloor)

        # Run script
        # win0 = []
        # door0 = []
        run1 = RunScript()
        # sc = run1.generate_script(win0, door0)
        building = connectIDA()
        # run1.apply_script(building, sc)
        sc2 = run1.generate_script(wins, doors)
        run1.apply_script(building,sc2)

    def testAdvDoors(self):
        # Doors from CSV
        df2 = pd.read_csv('d:\\untitled\\buildings\\doors.csv')
        doors = df2.to_dict(orient='records')
        for door in doors:
            door1 = door
            for key, val in door.copy().items():
                if pd.isnull(val):
                    door1.pop(key)
            door = door1




if __name__ == "__main__":
    wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                       13.899, 11.15, 9.98]
    _ceiling_ht = 3

    _test = TestRunScript()
    # test1.sw1_dw1_d1(2.6)
    # _test.testZoneCloneAND_DW(_ceiling_ht, wall_width_list)
    # test1.windowtwo(3)
    # _test.testScriptGene(_ceiling_ht, wall_width_list)
    # _test.testGene2()
    _test.testAdvWindow()