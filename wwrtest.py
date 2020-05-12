from util import *
import math
from basic import *
import runscript
from multiprocessing import Pool, Event,Queue
from multiprocessing import Process,Semaphore
import time
import readhtml

class WWRTest:
    def multiprocessing(self):
        sem = Semaphore(1)
        q = Queue()
        p_l = []
        for i in range(6):
            p = Process(target=self.runSimu, args=(q,i,sem))
            p.start()
            p_l.append(p)
            time.sleep(3)

        for i in p_l:
            i.join()

        print('============》')

        results = [q.get() for j in p_l]
        print(results)




    def runSimu(self,q, id, sem):
        sem.acquire()
        wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
        path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' + str(wwr[id]) + '.idm'
        building = connectIDA2(path)
        # before simulation ,check if it is ideal
        res1 = ida_checkstatus()
        if 'IDLE' in res1:
            runSimu(building)
            a = time.time()
        # Then creating the mathemaical model
        time.sleep(2)
        res1 = ida_checkstatus()
        if 'SIMULATING' in res1:
            b = time.time()
            time.sleep(1)
            sem.release()

        while True:
            res2 = ida_checkstatus()
            print('Tracking the program', str(wwr[id]), res2)
            if 'FINISHED' in res2:
                enda = time.time() - a
                endb = time.time() - b

                folder = 'D:\\ide_mine\\changing\\'
                base_model = 'ut1_7floorwithWin'
                idm = '.idm'
                readHTML = readhtml.Readhtml()
                readHTML.genehtml(building,folder,  base_model+'_'+str(wwr[id]))

                print('======> Simulation complete <======')
                print('Total time', enda)
                print('Simulation time', endb)
                break
            elif 'TERMINATED' in res2:
                print('******** Failed for ', str(wwr[id]), '*'*5)
                break
            time.sleep(2)





    def testWWRone(self, id=0):
        wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                           13.899, 11.15, 9.98]
        _ceiling_ht = 3

        wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]

        building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        for zone in zones:
            zone_val = zone['value']
            walls = call_ida_api_function(ida_lib.getChildrenOfType, zone_val, b"WALL")
            for i in range(len(walls)):
                wall_val = walls[i]['value']
                # wins = call_ida_api_function(ida_lib.getWindows, wall_val)
                wins = call_ida_api_function(ida_lib.getChildrenOfType, wall_val, b"WINDOW")
                # print(wins)
                sqrt_wwr = math.sqrt(wwr[0])
                win_wd = wall_width_list[i]*sqrt_wwr
                win_ht = _ceiling_ht*sqrt_wwr
                win_x = wall_width_list[i]/2 - win_wd/2
                win_y = _ceiling_ht/2 - win_ht/2
                newsize ={'X': win_x, 'Y': win_y, 'DX': win_wd, 'DY': win_ht}
                if type(wins) is list:
                    for win in wins:
                        win_val = win['value']
                        self.resizeWindow(win_val,newsize)



    def resizeWindows(self, zones):
        for zone in zones:
            # Windows are in walls
            windows = []
            walls = call_ida_api_function(ida_lib.getChildrenOfType, zone, b"WALL")

            for wall in walls:
                wall_val = wall['value']
                w_windows = call_ida_api_function(ida_lib.getChildrenOfType, wall_val, b"WINDOW")
                # if we get windows, add to windows list; there might be no windows
                if type(w_windows) is list:
                    for w_win in w_windows:
                        w_win_v = w_win['value']
                        windows.append(w_win_v)
            # Now we have all windows we want to resize
            for window in windows:
                dx = ida_get_named_child(window, "DX")
                dx_val = ida_get_value(dx)
                # We scale dx by 80%
                text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(0.8 * dx_val) + "}"
                res_h_l = call_ida_api_function(ida_lib.setAttribute, b"VALUE", dx, text_to_send.encode())

    def resizeWindow(self, win_obj, newsize):
        x = ida_get_named_child(win_obj, "X")
        x_val = ida_get_value(x)
        y = ida_get_named_child(win_obj, "Y")
        y_val = ida_get_value(y)
        dx = ida_get_named_child(win_obj, "DX")
        dx_val = ida_get_value(dx)
        dy = ida_get_named_child(win_obj, "DY")
        dy_val = ida_get_value(dy)
        print('value X', x_val,'; value Y', y_val, '; value DX', dx_val, '; value DY', dy_val)

        new_x = newsize['X']
        new_y = newsize['Y']
        new_dx = newsize['DX']
        new_dy = newsize['DY']

        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_dx) + "}"
        res_dx = call_ida_api_function(ida_lib.setAttribute, b"VALUE", dx, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_dy) + "}"
        res_dy = call_ida_api_function(ida_lib.setAttribute, b"VALUE", dy, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.1f}".format(new_y) + "}"
        res_y = call_ida_api_function(ida_lib.setAttribute, b"VALUE", y, text_to_send.encode())
        text_to_send = "{\"type\":\"number\",\"value\":" + "{0:.2f}".format(new_x) + "}"
        res_x = call_ida_api_function(ida_lib.setAttribute, b"VALUE", x, text_to_send.encode())

        print(res_dx, res_dy, res_x, res_y)

    # Use Lisp scripting method
    def testWWR2(self, sem, q, id=0):
        # Acquire semaphore
        sem.acquire()
        wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                           13.899, 11.15, 9.98]
        _ceiling_ht = 3

        wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
        wins = []
        doors = []
        for i in range(len(wall_width_list)):
            wall_name = 'WALL_'+str(i+1)
            sqrt_wwr = math.sqrt(wwr[id])
            win_wd = wall_width_list[i] * sqrt_wwr
            win_ht = _ceiling_ht * sqrt_wwr
            win_x = wall_width_list[i] / 2 - win_wd / 2
            win_y = _ceiling_ht / 2 - win_ht / 2
            newsize = {'wall_name': wall_name, 'win_x': win_x, 'win_y': win_y, 'win_dx': win_wd, 'win_dy': win_ht}
            wins.append(newsize)


        building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        runScript = runscript.RunScript()
        generated = runScript.generate_script(wins,doors,5, False)
        res = runScript.apply_script(building, generated)
        # print(res)
        path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' +str(wwr[id])+ '.idm'
        saveIDM(building, path)
        print('=============> NEXT <===============')

        # Release semaphore
        time.sleep(2)
        sem.release()

        simu_start = time.time()
        print("Simulation start......")
        runSimu(building)
        while True:
            res1 = ida_checkstatus()
            print(res1)
            if res1 == 'FINISHED':
                print('Simulation is done')
                break

            else:
                time.sleep(2)
                continue


        q.put(time.time()-simu_start)

    def seqprocessing(self):
        # base_building = connectIDA()
        for i in range(6):
            self.testWWR3(i)
            time.sleep(2)

        stat = ida_checkstatus()
        print(stat)



    def testWWR3(self, id=0):
        wall_width_list = [4, 7.5, 11.63, 10.27, 18.07, 20.587, 6.543, 8.72, 6.5176, 4, 6.48, 2.59, 31, 4, 9.886, 8.554,
                           13.899, 11.15, 9.98]
        _ceiling_ht = 3
        wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.35]
        wins = []
        doors = []
        for i in range(len(wall_width_list)):
            wall_name = 'WALL_'+str(i+1)
            sqrt_wwr = math.sqrt(wwr[id])
            win_wd = wall_width_list[i] * sqrt_wwr
            win_ht = _ceiling_ht * sqrt_wwr
            win_x = wall_width_list[i] / 2 - win_wd / 2
            win_y = _ceiling_ht / 2 - win_ht / 2
            newsize = {'wall_name': wall_name, 'win_x': win_x, 'win_y': win_y, 'win_dx': win_wd, 'win_dy': win_ht}
            wins.append(newsize)

        building = connectIDA()
        zones = call_ida_api_function(ida_lib.getZones, building)
        runScript = runscript.RunScript()
        generated = runScript.generate_script(wins,doors,5, False)
        res = runScript.apply_script(building, generated)
        # print(res)
        path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' +str(wwr[id])+ '.idm'
        saveIDM(building, path)
        time.sleep(1)
        print('=============> NEXT <===============')

        # wwr = [0.1, 0.15, 0.2, 0.25, 0.3, 0.4]
        # path = 'd:\\ide_mine\\changing\\ut1_7floorwithWin_wwr' + str(wwr[id]) + '.idm'
        # building = connectIDA2(path)
        # before simulation ,check if it is idle

        res1 = ida_checkstatus()
        print('check point', res1)
        # if 'IDLE' in str(res1):
        runEnergySimu(building)
        a = time.time()
        # Then creating the mathemaical model
        time.sleep(2)
        res1 = ida_checkstatus()
        if 'SIMULATING' in res1:
            b = time.time()
            time.sleep(1)
            # sem.release()

        while True:
            res2 = ida_checkstatus()
            print('Tracking the program', str(wwr[id]), res2)
            if 'FINISHED' in res2:
                enda = time.time() - a
                endb = time.time() - b
                saveIDM(building)
                folder = 'D:\\ide_mine\\changing\\'
                base_model = 'ut1_7floorwithWin'
                idm = '.idm'
                readHTML = readhtml.Readhtml()
                readHTML.genehtml(building, folder, base_model + '_' + str(wwr[id]))

                print('======> Simulation complete <======')
                print('Total time', enda)
                print('Simulation time', endb)
                break
            elif 'TERMINATED' in res2:
                print('******** Failed for ', str(wwr[id]), '*' * 5)
                break
            time.sleep(2)

        # else:
        #     print('*'*5,'Not idle, process finished')













if __name__ == "__main__":
    wwrTest = WWRTest()
    # wwrTest.testWWR2(1)
    # wwrTest.multiprocessing()
    # wwrTest.multiprocessing2()
    wwrTest.seqprocessing()