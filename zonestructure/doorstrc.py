"""One door !!!!   door_x : user-defined  door_y : default 0     door_dx: default 0.8     door_dy: default 2

    ( (ENCLOSING-ELEMENT :N WALL_6)
        (:ADD (OPENING :N "Door" :T OPENING)
        (:PAR :N X :V 3.21)
        (:PAR :N Y :V 1.8)       ;;default 0
        (:PAR :N DX :V 2)            ;;default 0.8
        (:PAR :N DY :V 2)           ;;default 2
        (:PAR :N CD_LO)
        )
      )

                    door_dx
           ____________________________
          |                           |
          |                           |
          |       Door                |
          |                           |
          |                            |    door_dy
          |___________________________|
  (door_x, door_y)

"""

class DoorStrc:

    # Predefine all required parameters
    def door_strc_merge(self, door):
        door_y = '0'
        door_dx = '0.8'
        door_dy = '2'
        if 'door_y' in door.keys():
            door_y = door['door_y']
        if 'door_dx' in door.keys():
            door_dx = door['door_dx']
        if 'door_dy' in door.keys():
            door_dy = door['door_dy']
        doorSc = self.door_strc(door['d_wall_name'], door['door_x'], door_y, door_dx, door_dy)
        return doorSc


    def door_strc(self, wall_name, door_x, door_y='0', door_dx='0.8', door_dy='2'):
        """
        :param wall_name: e.g. WALL_6
        :param door_x:
        :param door_y:
        :param door_dx:
        :param door_dy:
        :return: door_strc script
        """

        opening_heading = '( (ENCLOSING-ELEMENT :N ' + wall_name + ') (:ADD (OPENING :N "Door" :T OPENING)'
        opening_endnote = '(:PAR :N CD_LO)))'
        opening_par_x = '(:PAR :N X :V ' + door_x + ')'
        opening_par_y = '(:PAR :N Y :V ' + door_y + ')'  # default 0
        opening_par_dx = '(:PAR :N DX :V ' + door_dx + ')'  # default 0.8
        opening_par_dy = '(:PAR :N DY :V ' + door_dy + ')'  # default 2
        opening_tot = opening_heading + opening_par_x + opening_par_y + opening_par_dx + opening_par_dy + opening_endnote

        return opening_tot


# Unit test
if __name__ == "__main__":
    a = door_strc("WALL_6", "3.21")
    print(a)
