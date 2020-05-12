from util import *
import config
from collections import defaultdict
from os import path
import psutil
import time

""" 
        General basic methods :  connectIDA, saveIDM, disconnectIDA, 
                                showChildrenDict, showChildrenList, showChildrenListValue, 
                                showSingleChild, showChildrenByType
"""



def connectIDA(building_path = config.BUILDING_PATH):
    """
    :param: building_path
    :return: building:object
    """
    # Connecting to the IDA ICE API.
    pid = start()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, building_path.encode())
    return building,pid



def connectIDA2(building_path):
    """
    :param: building_path
    :return: building:object
    """
    # Connecting to the IDA ICE API.
    pid = start()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, building_path.encode())
    return building


def openIDM(building_path):
    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, building_path.encode())
    return building



def saveIDM(building, apath='', unpacked = 1):                         #packed:0 (default)   unpaced:1
    """
        Path empty: save;    Path: save as...
    """

    res1 = call_ida_api_function(ida_lib.saveDocument, building, apath.encode(), unpacked)            #b"D:\\ide_mine\\changing\\ut1_2.idm"
    if len(apath) > 0:
        if path.exists(apath):
            print('Successfully save file :', apath)
    return res1

def disconnectIDA(building):
    """
    :param building: object
    :return: end message:
    """
    saveIDM(building)
    end = ida_lib.ida_disconnect()
    return end

def runEnergySimu(building):
    res = call_ida_api_function_j(ida_lib.runSimulation, building, 2)
    print('Simulation begins. ')
    return res

def killprocess(pid):
    p = psutil.Process(int(pid))
    p.terminate()
    time.sleep(3)


# 应该新建dictionary 把东西列出来，避免重复寻找
def showChildrenDict(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    nameList = defaultdict(int)
    for child in children:
        name = ida_get_name(child['value'])
        nameList[child['value']] = name

    str(nameList)
    return nameList

def showChildrenList(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    nameList = []
    for child in children:
        name = ida_get_name(child['value'])
        nameList.append(name)

    str(nameList)
    return nameList


def showChildrenListValue(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    print("value:value")
    valueList =dict
    for child in children:
        name = ida_get_name(child['value'])
        value = ida_get_value(child['value'])
        valueList[child['value']]=value

    str(valueList)
    return valueList

def showSingleChild(parent, child_name):
    element = ida_get_named_child(parent, child_name)
    element_val = ida_get_value(element)
    print("The current %s value is %f, and the type is %s" %(child_name,element_val,type(element_val)))
    return element

def showChildrenByType(parent, child_type):
    """

    :param parent:
    :param child_type: ZONE, WINDOW, DET-WINDOW, OPENING
    :return: children: list
    """
    children = call_ida_api_function(ida_lib.getChildrenOfType, parent,child_type.encode())
    for i, val in enumerate(children):
        print("Child %s is %s" %(i,val))

    return children




#Unit test

def main():
    building = connectIDA()
    res = runSimu(building)
    print(res)


if __name__ == "__main__":
    main()
