"""
    Merge zone_strc, therm_bdg, door_strc, win_strc
"""
from zonestructure import thermbdg
from zonestructure import winstrc
from zonestructure import doorstrc

class ZoneStrc:

    def zone_strc_bsc(self, zone_name2):
        """
            ( (CE-ZONE :N "Zone 1")

                )
        :param zone_name:
        :return:
        """
        zone_strc_heading = '((CE-ZONE :N "' + zone_name2 + '")'
        zone_strc_endnote = ')'
        return zone_strc_heading, zone_strc_endnote


    # Zone based scripting, thermal bdgs, windows and doors
    def zone_strc(self, wins, doors, zone_name='Zone 1'):
        """

        :param wins: list of windows
        :param doors: list of doors
        :param zone_name: zone name, Zone 1, Zone 2
        :return: zone scripting
        """

        script_list = []
        zone_name1 = zone_name

        # zone heading and endnote
        zone_strc_heading, zone_strc_endnote = self.zone_strc_bsc(zone_name1)
        script_list.append(zone_strc_heading)

        # thermal bridge script
        win_num = len(wins)
        door_num = len(doors)
        therm_bdg_script = thermbdg.therm_bdg(win_num, door_num)
        script_list.append(therm_bdg_script)

        # Windows scripting
        win_list = []
        winStrc = winstrc.WinStrc()
        if len(wins) >0:
            for win in wins:     # loop for each window

                winSc = winStrc.win_strc_merge(win)
                win_list.append(winSc)
                # windowScript(self, wall_name, win_x, win_y, detailed_win=False, win_dx='2', win_dy='1', glazing=0):

        # Doors scripting
        door_list = []
        doorStrc = doorstrc.DoorStrc()
        if len(doors) >0:
            for door in doors:   # loop for each door

                doorSc = doorStrc.door_strc_merge(door)
                door_list.append(doorSc)


        script_list.append(' '.join(win_list))
        script_list.append(' '.join(door_list))
        script_list.append(zone_strc_endnote)
        res = ''.join(script_list)

        print(res)
        return res



# Unit test
if __name__ == "__main__":
    zoneStrc = ZoneStrc()
    wins = []
    doors = []
    win2 = {}
    win2['w_wall_name'] = 'WALL_13'
    win2['win_x'] = '26.015'
    win2['win_y'] = '0.8'
    win2['win_dx'] = '3'
    win2['win_dy'] = '1.8'
    win2['detailed'] = 1  # true 1   false 0
    win2['glazing'] = 1
    wins.append(win2)
    sc= zoneStrc.zone_strc(wins, doors, 'Zone 2')
    print(sc)