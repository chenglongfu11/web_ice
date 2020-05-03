from util import *

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
      
                    win_dx  default 1.2        
           ____________________________
          |                           |
          |      Window               |
          |                           |    win_dy default 1.5
          |___________________________|
  (win_x, win_y)
      """


def win_strc(wall_name, win_x, win_y, detailed=0, win_dx='1.2', win_dy='1.5', glazing=0):
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
    win_par_dx = '(:PAR :N DX :V ' + win_dx + ')'  # default 1.2
    win_par_dy = '(:PAR :N DY :V ' + win_dy + ')'  # default 1.5

    if detailed == 1:
        glazing_list = ['Double Clear Air (WIN7)', 'Single Clear (WIN7)', 'Double high solar gain low-e (WIN7)',
                       'Glazing-A_EN14501']
        win_glazing = '(:RES :N GLAZING :V "' + glazing_list[glazing] + '")'
        win_merge = win_det_heading + win_par_x + win_par_y + win_par_dx + win_par_dy + win_glazing + win_endnote

    else:
        win_merge = win_heading + win_par_x + win_par_y + win_par_dx + win_par_dy + win_endnote

    return win_merge





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




# Unit test
def main():
    # Connecting to the IDA ICE API.
    pid = start()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH[0])

    cloneWindow(building)

    end = ida_lib.ida_disconnect()


if __name__ == "__main__":
    main()
