"""
    Merge zone_strc, therm_bdg, door_strc, win_strc
"""
from . import therm_bdg
from . import win_strc
from . import door_strc

def zone_strc_bsc(zone_name):
    """
        ( (CE-ZONE :N "Zone 1")

            )
    :param zone_name:
    :return:
    """
    zone_strc_heading = '((CE-ZONE :N "' + zone_name + '")'
    zone_strc_endnote = ')'
    return zone_strc_heading, zone_strc_endnote


# Zone based scripting, thermal bdgs, windows and doors
def zone_strc(wins, doors, zone_name='Zone 1'):
    """

    :param wins: list of windows
    :param doors: list of doors
    :param zone_name: zone name, Zone 1, Zone 2
    :return: zone scripting
    """

    script_list = []
    zone_name1 = zone_name

    # zone heading and endnote
    zone_strc_heading, zone_strc_endnote = zone_strc_bsc(zone_name1)
    script_list.append(zone_strc_heading)

    # thermal bridge script
    win_num = len(wins)
    door_num = len(doors)
    therm_bdg_script = therm_bdg.therm_bdg(win_num, door_num)
    script_list.append(therm_bdg_script)

    # Windows scripting
    win_list = []
    for win in wins:     # loop for each window
        win_dx = '1.2'
        win_dy = '1.5'
        detailed1 = 0
        glazing = 0
        # win_x  win_y
        if 'win_dx' in win.keys():
            win_dx = win['win_dx']
        if 'win_dy' in win.keys():
            win_dy = win['win_dy']
        if 'detailed' in win.keys():
            detailed1 = win['detailed']
        if 'glazing' in win.keys():
            glazing = win['glazing']

        winSc = win_strc.win_strc(win['w_wall_name'], win['win_x'], win['win_y'], detailed1, win_dx, win_dy, glazing)

        win_list.append(winSc)
        # windowScript(self, wall_name, win_x, win_y, detailed_win=False, win_dx='2', win_dy='1', glazing=0):

    # Doors scripting
    door_list = []
    for door in doors:   # loop for each door
        door_y = '0'
        door_dx = '0.8'
        door_dy = '2'
        if 'door_y' in door.keys():
            door_y = door['door_y']
        if 'door_dx' in door.keys():
            door_dx = door['door_dx']
        if 'door_dy' in door.keys():
            door_dy = door['door_dy']

        doorSc = door_strc.door_strc(door['d_wall_name'], door['door_x'], door_y, door_dx, door_dy)
        door_list.append(doorSc)


    script_list.append(' '.join(win_list))
    script_list.append(' '.join(door_list))
    script_list.append(zone_strc_endnote)
    res = ''.join(script_list)

    print(res)
    return res