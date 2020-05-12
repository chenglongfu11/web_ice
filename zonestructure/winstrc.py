""" ONE window: simple window or detailed window
    The window is location based on the relative coordinates of the specific wall
    Carefully check if the window is inside the wall  

    ( (ENCLOSING-ELEMENT :N WALL_15)
        (:ADD (CE-WINDOW :N "DetWin" :T DET-WINDOW)    ;;detailed window
              (:PAR :N X :V 6.227)
              (:PAR :N Y :V 0.8)
              (:PAR :N DX :V 2)     ;;;;default 1.2
              (:PAR :N DY :V 1)     ;;default 1.5
              (:RES :N GLAZING :V "Double Clear Air (WIN7)")        ;;difference with simple win
              (:PAR :N LIGHT-LEVEL)
              (:PAR :N CD_LO)
          )
    )
      
     (   (ENCLOSING-ELEMENT :N WALL_13)
            (:ADD (CE-WINDOW :N "Window" :T WINDOW)
                  (:PAR :N X :V 25.026)
                  (:PAR :N Y :V 0.8)
                  (:PAR :N DX :V 1.5)
                  (:PAR :N DY :V 1.6)
                  (:RES :N GLAZING :V "3 pane glazing, clear, 4-12-4-12-4")      ;;glaing material
                  (:PAR :N INTERNAL_SHADING-CONTROL :V NONE)      ;; shading control
                  (:PAR :N LIGHT-LEVEL :F 0)
                  (:PAR :N OPENING-CONTROL :V SCHEDULE)            
                  (:RES :N OPENING-SCHEDULE :F 0 :V "07-17 weekdays")   ;;  :V ALWAYS_ON    0
                  (:PAR :N CD_LO)
                  (   (WALL-PART :N FRAME)                ;;material parameters
                      (:PAR :N AREA_FRACTION :V 0.2)
                      (:PAR :N U-VALUE :V 3.0)
                   )
            )
    )
    

                    win_dx  default 1.2        
           ____________________________
          |                           |
          |      Window               |
          |                           |    win_dy default 1.5
          |___________________________|
  (win_x, win_y)

  win: wall_name, win_x, win_y, win_dx, win_dy, detailed, glazing, shading, recess, schedule, material
                schedule: plan_type, start, end ( plan_type: 3:ALWAYS_ON 4:0 always off
                material: area_fraction, u_value

      """
from util import *
import pandas as pd


class WinStrc:
    # Predefine all required parameters
    def wins_merge(self, wins, add = True):
        """
            The updated method merge several windows on one wall into one ENCLOSING-ELEMENT script
        :param wins: list of windows : win: wall_name, win_x, win_y, win_dx, win_dy, detailed, glazing, shading, recess, schedule, material

        :return: merged script
        """
        wall_name_ls = []
        strc_ls = []
        for win in wins:
            wall_nm = win['wall_name']
            if wall_name_ls.count(wall_nm) > 0:
                index = wall_name_ls.index(wall_nm)
                strc_ls[index]['number'] += 1
                strc_ls[index]['script'] += self.win_strc2(win, add, str(strc_ls[index]['number']-1))
            else:
                strc_heading = '( (ENCLOSING-ELEMENT :N ' + wall_nm + ')'
                wall_name_ls.append(wall_nm)
                win_strc_script = self.win_strc2(win, add)
                strc_ls.append({'script': strc_heading + win_strc_script, 'number': 1})

        strc_endnote = ')'
        for ele in strc_ls:
            ele['script'] += strc_endnote

        output_script = ' '.join(ele['script'] for ele in strc_ls)
        return output_script

    def win_strc2(self, win, new = True, num = ''):
        """

        :param win: wall_name, win_x, win_y, win_dx, win_dy, detailed, glazing, shading, recess, schedule, material
                schedule: plan_type, start, end
                material: area_fraction, u_value
        :return:
        """
        strc_list = []
        add = ':ADD'
        if not new:
            add = ''

        # strc_heading = '( (ENCLOSING-ELEMENT :N ' + win['wall_name'] + ') (:ADD (CE-WINDOW :N "Window" :T WINDOW) '
        strc_heading = '(' + add +' (CE-WINDOW :N "Window' + str(num) + '" :T WINDOW) '
        strc_list.append(strc_heading)
        strc_ll = '(:PAR :N LIGHT-LEVEL) (:PAR :N CD_LO)'
        strc_endnote = ')'
        strc_x = '(:PAR :N X :V ' + str(win['win_x']) + ')'
        strc_y = '(:PAR :N Y :V ' + str(win['win_y']) + ')'
        strc_list.append(strc_x)
        strc_list.append(strc_y)

        # win_dx  win_dy
        win_dx = 1.2
        win_dy = 1.5
        if 'win_dx' in win.keys():
            win_dx = win['win_dx']
        if 'win_dy' in win.keys():
            win_dy = win['win_dy']
        strc_dx = '(:PAR :N DX :V ' + str(win_dx) + ')'  # default 1.2
        strc_dy = '(:PAR :N DY :V ' + str(win_dy) + ')'  # default 1.5
        strc_list.append(strc_dx)
        strc_list.append(strc_dy)

        detailed1 = 0
        glazing = 0
        if 'detailed' in win.keys():
            detailed1 = win['detailed']
            if 'glazing' in win.keys():
                glazing = int(win['glazing'])
            if detailed1 == 1:
                strc_heading = '(' + add + ' (CE-WINDOW :N "DetWin' + str(num) +'" :T DET-WINDOW) '  # detailed window
                glazing_list = ['Double Clear Air (WIN7)', 'Single Clear (WIN7)', 'Double high solar gain low-e (WIN7)',
                                'Glazing-A_EN14501', '3 pane glazing, clear, 4-12-4-12-4']   # TODO: more materials
                strc_glazing = '(:RES :N GLAZING :V "' + glazing_list[glazing] + '")'
                strc_list[0] = strc_heading
                strc_list.append(strc_glazing)

        shading_ctrl = 'NONE'
        if 'shading' in win.keys():
            shading_ctrl = win['shading']
            strc_shading = self.shading(shading_ctrl)
            strc_list.append(strc_shading)

        strc_ll = '(:PAR :N LIGHT-LEVEL) (:PAR :N CD_LO) '
        strc_list.append(strc_ll)


        if 'schedule' in win.keys():
            schedule = win['schedule']                                   # dict
            # shd, shd_name = self.schedule_rule(schedule)
            strc_opening_ctrl = self.opening_ctrl(schedule)
            strc_list.append(strc_opening_ctrl)

        recess_dpt = 0
        if 'recess' in win.keys():
            recess_dpt = win['recess']
            reces = self.recess(recess_dpt)
            strc_list.append(reces)

        u_value = 2
        area_frac = 0.1
        if 'material' in win.keys():
            material = win['material']
            strc_mt = self.materials(material)
            strc_list.append(strc_mt)

        strc_list.append(strc_endnote)
        winSc = ' '.join(strc_list)
        # winSc = self.win_strc(win['w_wall_name'], win['win_x'], win['win_y'], win_dx, win_dy, detailed1, glazing)
        return winSc

    # Basic function, Not used
    def win_strc(self, wall_name, win_x, win_y, win_dx=1.2, win_dy=1.5, detailed=0, glazing=0):
        """

        :param wall_name:
        :param win_x:
        :param win_y:
        :param detailed: if detailed window
        :param win_dx: default 1.2
        :param win_dy: default 1.5
        :param glazing: if detailed window, specify glazing type
        :return: win_strc script for one window
        """

        win_det_heading = '( (ENCLOSING-ELEMENT :N ' + wall_name + ') (:ADD (CE-WINDOW :N "DetWin" :T DET-WINDOW) '    #detailed window
        win_heading = '( (ENCLOSING-ELEMENT :N ' + wall_name + ') (:ADD (CE-WINDOW :N "Window" :T WINDOW) '
        win_endnote = '(:PAR :N LIGHT-LEVEL) (:PAR :N CD_LO) )  )'
        win_par_x = '(:PAR :N X :V ' + win_x + ')'
        win_par_y = '(:PAR :N Y :V ' + win_y + ')'
        win_par_dx = '(:PAR :N DX :V ' + str(win_dx) + ')'  # default 1.2
        win_par_dy = '(:PAR :N DY :V ' + str(win_dy) + ')'  # default 1.5

        if detailed == 1:
            glazing_list = ['Double Clear Air (WIN7)', 'Single Clear (WIN7)', 'Double high solar gain low-e (WIN7)',
                           'Glazing-A_EN14501']       # TODO: more materials
            win_glazing = '(:RES :N GLAZING :V "' + glazing_list[glazing] + '")'
            win_merge = win_det_heading + win_par_x + win_par_y + win_par_dx + win_par_dy + win_glazing + win_endnote

        else:
            win_merge = win_heading + win_par_x + win_par_y + win_par_dx + win_par_dy + win_endnote

        return win_merge

    # Not used
    def schedule_rule(self, schedule):
        """
            (:ADD (SCHEDULE-DATA :N "07-17 weekdays" :T SCHEDULE-DATA :D "On weekdays 7-17, otherwise off" :QT FACTOR)
              (SCHEDULE-RULE :N "weekdays 7-17" :T SCHEDULE-RULE :D NIL :RESTRICTION #(1 1 1 1 1 0 0) :VALUE (7 0 17 0 1 0.0))   ;;(6 0 18 0 1 0.0))
              (SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE 0 :INDEX 1)
            )

            (:ADD (SCHEDULE-DATA :N "08-17 every day" :T SCHEDULE-DATA :D "On every day 8-17, otherwise off" :QT FACTOR)
                  (SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE (8 0 17 0 1))
            )
        :param schedule: plan_type 1:weekdays only 2:every day 3:ALWAYS_ON 4:0 always off
                        start
                        end
        :return:
        """

        if schedule['plan_type'] == 1:
            time = str(schedule['start'])+'-'+ str(schedule['end'])
            shd_p1 = ' (:ADD (SCHEDULE-DATA :N "' + time +' weekdays" :T SCHEDULE-DATA :D "On weekdays '+time + \
                     ', otherwise off" :QT FACTOR)'
            shd_p2 = '(SCHEDULE-RULE :N "weekdays '+ time +'" :T SCHEDULE-RULE :D NIL :RESTRICTION #(1 1 1 1 1 0 0) :VALUE (' + \
                     str(schedule['start']) + ' 0 '+str(schedule['end'])+' 0 1 0.0))'
            shd_p3 = '(SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE 0 :INDEX 1)'
            shd_p4 = ')'
            shd_tot = shd_p1 + shd_p2 + shd_p3 + shd_p4
            shd_name = time + ' weekdays'

        elif schedule['plan_type'] == 2:
            time = str(schedule['start']) + '-' + str(schedule['end'])
            shd_p1 = '(:ADD (SCHEDULE-DATA :N "' + time +' every day" :T SCHEDULE-DATA :D "On every day '+time+\
                     ', otherwise off" :QT FACTOR)'
            shd_p2 = '(SCHEDULE-RULE :N DEFAULT :T SCHEDULE-RULE :D NIL :VALUE (' + str(schedule['start'])+' 0 '+str(schedule['end'])+' 0 1))'
            shd_p3 = ')'
            shd_tot = shd_p1 + shd_p2 + shd_p3
            shd_name = time + ' every day'

        elif schedule['plan_type'] == 3:
            shd_tot = ''
            shd_name = 'ALWAYS_ON'

        else:
            shd_tot = ''
            shd_name = '0'

        return shd_tot, shd_name


    def opening_ctrl(self, schedule):    #default 0
        """
            !!! The only available functions are 3:ALWAYS_ON and 4 0
            (:PAR :N OPENING-CONTROL :V SCHEDULE)
            (:RES :N OPENING-SCHEDULE :F 0 :V "07-17 weekdays")   ;;  :V ALWAYS_ON    0
        :param: plan_type 1:weekdays only 2:every day 3:ALWAYS_ON  4:0 always off (default)
        :param: start
        :param: end
        :return:
        """
        opening_ctrl_p1 = '(:PAR :N OPENING-CONTROL :V SCHEDULE)'
        if schedule['plan_type'] == 1:
            time = str(schedule['start']) + '-' + str(schedule['end'])
            name = time + ' weekdays'
            opening_ctrl_p2 = '(:RES :N OPENING-SCHEDULE :F 0 :V "' + name + '")'
        elif schedule['plan_type'] == 2:
            time = str(schedule['start']) + '-' + str(schedule['end'])
            name = time + ' every day'
            opening_ctrl_p2 = '(:RES :N OPENING-SCHEDULE :F 0 :V "' + name + '")'
        elif schedule['plan_type'] == 3:
            name = 'ALWAYS_ON'
            opening_ctrl_p1 = '(:PAR :N OPENING-CONTROL :V ALWAYS_ON)'
            opening_ctrl_p2 = '(:RES :N OPENING-SCHEDULE :F 0 :V ' + name + ')'
        else:
            opening_ctrl_p1 = ''
            name = '0'
            opening_ctrl_p2 = ''

        # opening_ctrl_p1 = '(:PAR :N OPENING-CONTROL :V SCHEDULE)'
        # opening_ctrl_p2 = '(:RES :N OPENING-SCHEDULE :F 0 :V "' + name + '")'

        return opening_ctrl_p1+opening_ctrl_p2


    def recess(self, par = 0):        #default 0
        """
            (:PAR :N RECESS :V 1)   ;;凹陷深度
        :param par: recess depth
        :return:
        """
        return '(:PAR :N RECESS :V ' + str(par) + ')'

    def shading(self, type = 'NONE'):    # default NONE
        """
            (:PAR :N INTERNAL_SHADING-CONTROL :V NONE)      ;; shading control
        :param type:
        :return:
        """
        return '(:PAR :N INTERNAL_SHADING-CONTROL :V '+type+')'

    def materials(self, material):
        """
          (   (WALL-PART :N FRAME)                ;;material parameters
               (:PAR :N AREA_FRACTION :V 0.2)
               (:PAR :N U-VALUE :V 3.0)
          )

        :param material: area_fraction    u_value
        :return: 
        """

        area_frac = 0.1     # range 0-1  default 0.1
        u_val = 2.0         # default 2.0
        if material['area_fraction']:
            area_frac = material['area_fraction']
        if material['u_value']:
            u_val = material['u_value']

        mt_p1 = '( (WALL-PART :N FRAME) '
        mt_p2 = '(:PAR :N AREA_FRACTION :V ' + str(area_frac) + ') '
        mt_p3 = '(:PAR :N U-VALUE :V ' + str(u_val) + ')'
        mt_p4 = ')'

        return mt_p1+mt_p2+mt_p3+mt_p4







# Not used
def findWall(building):
    zones = call_ida_api_function(ida_lib.getChildrenOfType, building, b"ZONE")
    for zone in zones:
        zone_name = ida_get_name(zone['value'])
        print(str(zone_name))
    zone2 = ida_get_named_child(building, "Zone")
    print("Zone 2 is " + str(zone2))
    if zone2 == False:
        print("Wrong name of zone")
        return False
    else:
        wall2 = ida_get_named_child(zone2, "WALL_2")
        if wall2 == False:
            print("Wrong name of Wall")
            return False
        else:
            return wall2
    return False

#Not used
def cloneWindow(building):
    wall2 = findWall(building)
    if wall2 == False:
        print("clone is unsuccessful due to missing wall")
    else:

        ref_windows = call_ida_api_function(ida_lib.getWindows, building)
        # cloned_Window = call_ida_api_function(ida_lib.copyObject, ref_windows[0]['value'], b"Window added2")
        parent = call_ida_api_function(ida_lib.parentNode, cloned_Window)
        name_parent = ida_get_name(parent)
        print("the name of previous parent is " + str(name_parent))
        call_ida_api_function(ida_lib.removeChild, cloned_Window, parent)

        # new_parent = call_ida_api_function(ida_lib.setParentNode, ref_windows[0]['value'], wall2)
        # print("the new parent is "+str(ida_get_name(new_parent)))

        # newChildren = call_ida_api_function(ida_lib.appendChild, ref_windows[0]['value'], wall2)

        # for node in newChildren:
        #     print("The node %s is %s " % (node['value'], ida_get_name(node['value'])))
    # firstWindow = call_ida_api_function(ida_lib.copyObject, windows[0]['value'],b"Window 11")

    # call_ida_api_function(ida_lib.setParentNode, new_window, wall2)


def main():
    # Connecting to the IDA ICE API.
    pid = start()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH[0])

    cloneWindow(building)

    end = ida_lib.ida_disconnect()




# Unit test
class TestWinstrc:

    def testWinsMerge(self):
        materials = {'area_fraction': 0.5, 'u_value': 5}
        df = pd.read_csv('d:\\untitled\\buildings\\windows.csv')
        wins = df.to_dict(orient='records')
        for win in wins:
            win1 = win
            for key, val in win.copy().items():
                if pd.isnull(val):
                    win1.pop(key)
            win = win1
            # win['schedule'] = schedules
            win['material'] = materials

        winStrc = WinStrc()
        sc = winStrc.wins_merge(wins)
        print(sc)




if __name__ == "__main__":
    test = TestWinstrc()
    test.testWinsMerge()
