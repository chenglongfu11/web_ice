""" ALL thermal bridges for doors and windows

    ( (AGGREGATE :N THERMAL-BRIDGES)
        (:PAR :N WIN-PERIM-LEN)
        (:PAR :N DOOR-PERIM-LEN)
        )
"""


def therm_bdg(win_num=0, door_num=0):
    if win_num == 0 and door_num == 0:
        return ''

    therm_bdg_heading = '( (AGGREGATE :N THERMAL-BRIDGES) '
    therm_bdg_end = ')'
    therm_bdg_win = '(:PAR :N WIN-PERIM-LEN)'  # both det windows and simple windows
    therm_bdg_door = '(:PAR :N DOOR-PERIM-LEN)'

    therm_bdg_merge = therm_bdg_heading + therm_bdg_win * win_num + therm_bdg_door * door_num + therm_bdg_end
    return therm_bdg_merge


# Unit test
if __name__ == "__main__":
    a = therm_bdg(2, 1)
    print(a)
