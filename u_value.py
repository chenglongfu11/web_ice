from util import *
from webproject.webapplication import showList
import os
import win32api
import win32process


# The U value range is 0.. 5.9
# 现在的问题：关闭之后，U value会回到1.9

def openProgram():
    path_to_ice = config.APP_PATH
    command = path_to_ice + "ida-ice.exe \"" + path_to_ice + "ida.img\" -G 1"
    startObj = win32process.STARTUPINFO()
    ret = win32process.CreateProcess(None, command, None, None, 0, 0, None, None, startObj)
    newpid = str(ret[2])
    time.sleep(5)
    # Add path_to_ice to PATH variable, is removed when program finishes
    os.environ['PATH'] = path_to_ice + os.pathsep + os.environ['PATH']

    test = ida_lib.connect_to_ida(b"5945", newpid.encode())


def check_process(process_name):
    try:
        print("tasklist | findstr " + process_name)
        process = len(os.popen('tasklist | findstr ' + process_name).readlines())
        print(process)
        if process >= 1:
            return True
        else:
            return False
    except:
        print("The program is wrong")
        return False


def changeUvalue(building, newU=2):
    glazing = ida_get_named_child(building, "3 pane glazing, clear, 4-12-4-12-4")
    u_value = showList.showSingleChild(glazing, "U")
    text_to_send = "{\"type\":\"number\",\"value\":" +"{0:.1f}".format(newU) + "}"
    res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", u_value, text_to_send.encode())
    ress = ida_get_value(u_value)
    if ress == newU:
        print("Succefully changed building height to  %s" %newU)
        return True
    else:
        print("Error in changing building height")
        return False


def copyFile(str="d:\\ide_mine\\test_building3.idm"):
    # 获取文件名
    file_path = str
    path_idx = file_path.rfind("\\")   # 路径标识截取
    file_path_1 = file_path[:path_idx + 1]  # 截取路径
    file_name = file_path[path_idx + 1:]  # 截取文件名
    # 判断并确定新的文件名
    idx = file_name.rfind(".")
    file_name_1 = file_name[:idx]  # 文件名前半段
    file_name_2 = file_name[idx:]  # 文件名后半段
    new_file_name = ''
    # 判断副本文件是否存在
    if os.path.exists(file_path_1 + file_name_1 + "copy" + file_name_2) == False:
        new_file_name = file_path_1 + file_name_1 + "copy" + file_name_2
    else:
        for i in range(2, 100):
            # 判断副本（i）文件是否存在
            if os.path.exists(file_path_1 + file_name_1 + "copy{}".format(i) + file_name_2) == False:
                new_file_name = file_path_1 + file_name_1 + "copy{}".format(i)+ file_name_2
                break
            else:
                i += 1
                continue

    # 复制程序开始
    file = open(file_path, "rb")
    file1 = open(new_file_name, "wb")
    while True:
        info = file.read(1024)
        if not info:
            break
        file1.write(info)
    file.close()
    file1.close()  # 复制程序结束

    print(os.listdir(file_path_1))
    return new_file_name



def main():
    new_file = copyFile()
    # Connecting to the IDA ICE API.

    # 战略性comment
    # win32api.ShellExecute(0,
    #                     '',
    #                     r'D:\idaice\bin\ice.exe',
    #                     r'-Q -R D:\ide_mine\test_building3.idm',
    #                     '',
    #                     1)
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    building_2 = call_ida_api_function(ida_lib.openDocument, new_file.encode())
    changeUvalue(building_2)
    call_ida_api_function(ida_lib.saveDocument,building_2,b"",1)
    call_ida_api_function(ida_lib.exitSession)

    win32api.ShellExecute(0,
                        '',
                        r'D:\idaice\bin\ice.exe',
                        "-Q -R "+new_file,
                        '',
                        1)

    proc_is_exist = True
    while (proc_is_exist):
        if check_process('ida-ice.exe'):
            proc_is_exist = True
            time.sleep(20)
            print("still running")
        else:
            proc_is_exist = False

    openProgram()

    # Open a saved building
    building = call_ida_api_function(ida_lib.openDocument, b"d:\\ide_mine\\test_building3.idm")
    building_2 = call_ida_api_function(ida_lib.openDocument, new_file.encode())
    # print("the building is %d" %building )
    # print("the building is %d" % building_2)

    energy_report = ida_get_named_child(building, "ENERGY-REPORT")
    rep_res = call_ida_api_function(ida_lib.printReport,energy_report,b"d:\\ide_mine\\1.pdf",2)
    print("Printing report {}".format(rep_res))


    # changeUvalue(building_2)
    # run_simu.do_simulation(building_2)
    energy_report_2 = ida_get_named_child(building_2, "ENERGY-REPORT")
    rep_res_2 = call_ida_api_function(ida_lib.printReport,energy_report_2, b"d:\\ide_mine\\2.pdf",2)
    print("Printing report {}".format(rep_res_2))

    text_to_send = "[{\"type\":\"object\",\"value\":" +"{0:.0f}".format(building) + \
                   "},{\"type\":\"object\",\"value\":"+"{0:.0f}".format(building_2)+"}]"
    res_h_l = call_ida_api_function(ida_lib.compareResults, text_to_send.encode(),b"d:\\ide_mine\\3.pdf",2)

def main2():
    new_file = copyFile()
    test = ida_lib.connect_to_ida(b"5945", pid.encode())
    building_2 = call_ida_api_function(ida_lib.openDocument, new_file.encode())
    changeUvalue(building_2,3)
    call_ida_api_function(ida_lib.saveDocument,building_2,b"",1)
    # call_ida_api_function(ida_lib.exitSession)

    # win32api.ShellExecute(0,
    #                     '',
    #                     r'D:\idaice\bin\ice.exe',
    #                     "-Q -R "+new_file,
    #                     '',
    #                     1)






if __name__ == "__main__":
    main2()
