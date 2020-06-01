from util import *
import config

# 应该新建dictionary 把东西列出来，避免重复寻找
def showChildrenList(parent):
    children = call_ida_api_function(ida_lib.childNodes, parent)
    print("value:name")
    nameList = dict
    for child in children:
        name = ida_get_name(child['value'])
        nameList[child['value']]=name

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
    children = call_ida_api_function(ida_lib.getChildrenOfType, parent,child_type.encode())
    for i, val in enumerate(children):
        print("Child %s is %s" %(i,val))

    return children



def main():
    # Connecting to the IDA ICE API.
    pid=start()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, config.BUILDING_PATH)
    print("the building is %d" %building )
    showChildrenList(building)
    print(str(ida_get_name(building)))



    # zones = showChildrenByType(building, "ZONE")
    # for i, val in enumerate(zones):
    #
    #     geometry = ida_get_named_child(val['value'], "GEOMETRY")
    #     showSingleChild(geometry,"CEILING-HEIGHT")
    #     # showChildrenList(geometry)


    end = ida_lib.ida_disconnect()


if __name__ == "__main__":
    main()
