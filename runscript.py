from util import *
import config
from zonestructure import winstrc, thermbdg, doorstrc
import zoneclone
from zonestructure import zonestrc
from basic import *
import schedulestrc


class RunScript:
    #TODO
    def manage_csv(self, csv_path):
        pass

    def apply_script(self, building, script):
        res = call_ida_api_function_j(ida_lib.runIDAScript, building, script.encode())
        print('Apply_script message: ',res)
        return res

    # Aggregated scripting generator    wins each floor, doors each floor
    def generate_script(self, wins, doors, num_zone=1, add=True):
        scriptList = []
        heading, endnote = self.script_bsc()
        scriptList.append(heading)

        # # schedule structure
        # existing_shd = []
        # if len(wins) ==0 and len(doors) == 0:
        #     for win in wins:
        #         if 'schedule' in win.keys():
        #             shd = win['schedule']
        #             exist = False
        #             for e_shd in existing_shd:
        #                 if shd == e_shd:
        #                     exist = True
        #
        #             if not exist:
        #                 shd_ls, nm = schedulestrc.schedule_rule(shd)
        #                 scriptList.append(shd_ls)

        #TODO zone structure
        for i in range(num_zone):
            zone_name1 = 'Zone ' + str(i + 1)
            _zoneStrc = zonestrc.ZoneStrc()
            zoneScrip = _zoneStrc.zone_strc(wins, doors, zone_name1, add)
            scriptList.append(zoneScrip)

        scriptList.append(endnote)
        ressss = ' '.join(scriptList)
        print('Generated script: ',ressss)
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


