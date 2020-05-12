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

      ;;construction: NONE, when none, shcedule is always_on. ela=1
      (:ADD (OPENING :N "Door" :T OPENING)
            (:PAR :N X :V 4.266)
            (:RES :N OPENING-SCHEDULE :F 2564 :V ALWAYS_ON)
            (:ORES :N CONSTRUCTION :V :NONE)
            (:RES :N INTERNAL_SURFACE :F 2564)
            (:RES :N EXTERNAL_SURFACE :F 2564)
            (:PAR :N ELA :V 1)
            (:PAR :N CD_LO)
      )
    ;;construction: furniture, ela=1, shceudle is always_on
    (:ADD (OPENING :N "Door" :T OPENING)
          (:PAR :N X :V 4.266)
          (:RES :N OPENING-SCHEDULE :V ALWAYS_ON)
          (:ORES :N CONSTRUCTION :V STD-FURNITURE)    ;;"Inner door"   "Entrance door"
          (:PAR :N ELA :V 1)
          (:PAR :N CD_LO)
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

    construction: 1=defualt[use wall construction], 2=NONE(no door), 3=STD-FURNITURE, 4="Entrance door" 5="Inner door"
    schedule: 1 = always off, 2= always on
    ela: value

"""

class DoorStrc:
    def doors_merge(self, doors):

        wall_name_ls = []
        strc_ls = []
        for door in doors:
            wall_nm = door['wall_name']
            if wall_name_ls.count(wall_nm) > 0:
                index = wall_name_ls.index(wall_nm)
                strc_ls[index]['number'] += 1
                strc_ls[index]['script'] += self.door_strc(door, str(strc_ls[index]['number']-1))
            else:
                strc_heading =  '( (ENCLOSING-ELEMENT :N ' + wall_nm + ')'
                wall_name_ls.append(wall_nm)
                door_strc_script = self.door_strc(door)
                strc_ls.append(({'script': strc_heading + door_strc_script, 'number' : 1})
                               )

        strc_end = ')'
        for ele in strc_ls:
            ele['script'] += strc_end

        output_script = ' '.join(ele['script'] for ele in strc_ls)
        return output_script




    def door_strc(self, door, num = ''):
        """
        :param door: wall_name: e.g. WALL_6, door_x, door_y: default '0', door_dx: default '0.8', door_dy: default '2'
                    construction: 1,2,3,4,    schedule: 1,2    ela: default 0.01
        :param num on each wall
        :return: door_strc script
        """
        script_ls =[]
        opening_heading = '(:ADD (OPENING :N "Door' + str(num) + '" :T OPENING)'
        opening_endnote = '(:PAR :N CD_LO))'

        door_y = '0'
        door_dx = '0.8'
        door_dy = '2'
        opening_par_x = '(:PAR :N X :V ' + str(door['door_x']) + ')'
        script_ls.append(opening_heading)
        script_ls.append(opening_par_x)
        if 'door_y' in door.keys():
            door_y = door['door_y']
            opening_par_y = '(:PAR :N Y :V ' + str(door_y) + ')'  # default 0
            script_ls.append(opening_par_y)
        if 'door_dx' in door.keys():
            door_dx = door['door_dx']
            opening_par_dx = '(:PAR :N DX :V ' + str(door_dx) + ')'  # default 0.8
            script_ls.append(opening_par_dx)
        if 'door_dy' in door.keys():
            door_dy = door['door_dy']
            opening_par_dy = '(:PAR :N DY :V ' + str(door_dy) + ')'  # default 2
            script_ls.append(opening_par_dy)

        if 'construction' in door.keys():
            constr = door['construction']
            if constr == 2:    #no door
                script_ls.append("(:RES :N OPENING-SCHEDULE :F 2564 :V ALWAYS_ON) (:ORES :N CONSTRUCTION :V :NONE) (:RES :N INTERNAL_SURFACE :F 2564)  (:RES :N EXTERNAL_SURFACE :F 2564)")
            elif constr == 1:  # default(use wall construction
                if 'schedule' in door.keys():
                    shd = door['schedule']
                    if shd == 2:
                        script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")
            elif constr ==3:  # use std-furniture
                if 'schedule' in door.keys():
                    shd = door['schedule']
                    if shd == 2:
                        script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")
                script_ls.append("(:ORES :N CONSTRUCTION :V STD-FURNITURE)")
            elif constr == 4:   # 4="Entrance door"
                if 'schedule' in door.keys():
                    shd = door['schedule']
                    if shd == 2:
                        script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")
                script_ls.append('(:ORES :N CONSTRUCTION :V "Entrance door")')
            elif constr == 5:   # 5="Inner door"
                if 'schedule' in door.keys():
                    shd = door['schedule']
                    if shd == 2:
                        script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")
                script_ls.append('(:ORES :N CONSTRUCTION :V "Inner door")')
            else:
                if 'schedule' in door.keys():
                    shd = door['schedule']
                    if shd == 2:
                        script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")
        else:
            if 'schedule' in door.keys():
                shd = door['schedule']
                if shd == 2:
                    script_ls.append("(:RES :N OPENING-SCHEDULE :V ALWAYS_ON)")

        if 'ela' in door.keys():   #default 0.01
            ela_val = door['ela']

            script_ls.append('(:PAR :N ELA :V '+str(ela_val)+')')
        script_ls.append(opening_endnote)

        opening_tot = ' '.join(script_ls)

        return opening_tot


# Unit test
# if __name__ == "__main__":
