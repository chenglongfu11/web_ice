import plotly.graph_objects as go
import pandas as pd
from basic import *
import time
import readhtml


class Simulation:

    def simulation_bld(self, building, path):
        """
            存在一个死循环，必须让simulation完成，不是特别好？
        :param building:
        :param path: used to track the program's name
        :return:
        """
        file_name = path.split('\\')[-1]


        while True:
            res1 = ida_checkstatus()
            print('-' * 15)
            print('Check point before simulation', res1)
            failtime = 0

            if 'IDLE' in str(res1):
                start_time = time.time()  # Creating math model  -- simulation
                runEnergySimu(building)
                time.sleep(2)

                # Track simulation status
                res1 = ida_checkstatus()
                if 'SIMULATING' in res1:  # Check if simulating start successfully
                    start_time_simu = time.time()
                    time.sleep(1)

                    count = 0
                    while True:
                        res2 = ida_checkstatus()

                        if 'FINISHED' in res2:
                            enda = time.time() - start_time
                            endb = time.time() - start_time_simu
                            saveIDM(building)

                            print('======> Simulation complete <======')
                            print('Total time', enda)
                            print('Simulation time', endb)
                            print('-' * 15)
                            return True, enda, endb
                        elif 'TERMINATED' in res2:
                            print('******** Failed for simulation', file_name, '*' * 8)
                            print('Please check errors in GUI and restart the simulation manually')
                            time.sleep(2)

                            return False, 0, 0

                        count += 1
                        if count == 10:
                            print('Simulation tracking', file_name, ':', res2, '. Time consumed: ',
                                  time.time()-start_time_simu)
                            count = 0
                        time.sleep(2)

                else:
                    print('******** Failed for simulation', file_name, '*' * 8)
                    print('Please check errors in GUI and restart the simulation manually')
                    time.sleep(2)

                    return False, 0, 0

            else:
                time.sleep(2)
                if failtime == 5:
                    print('******** Failed for simulating', file_name, '*' * 8)
                    print('Please check errors in GUI and restart the simulation manually')
                    time.sleep(2)

                    return False, 0, 0

                failtime += 1
                continue


    # Call the building object from path and run the simulation
    def simulation_path(self, folder, base, wwr):
        idm = '.idm'
        path = folder + base + '_wwr' + str(wwr) + idm
        building, pid = connectIDA(path)
        res1, res2, res3 = self.simulation_bld(building, path)
        if res1:
            dict = {'wwr_ratio': wwr, 'total_time': res2, 'simu_time': res3}
            bld_dict = {'wwr_ratio': wwr, 'building': building}
            return dict, bld_dict


    # Call the building object from path and run the simulation. If simulation is complete, html report is generated
    def simulation_path_w_html(self, folder, base, wwr):
        idm = '.idm'
        path = folder + base + '_wwr' + str(wwr) + idm
        filename = base+ '_wwr' + str(wwr)
        building, pid = connectIDA(path)
        res1, res2, res3 = self.simulation_bld(building, path)
        readHTML = readhtml.Readhtml()
        if res1:
            dict = {'wwr_ratio': wwr, 'total_time': res2, 'simu_time': res3}
            html_path = readHTML.genehtml_bld(building, folder, filename)
            html_dict = {'wwr_ratio': wwr, 'html': html_path}
            return dict,html_dict



    def sequantial_simulation(self, folder, base, wwrs):
        """
        :param folder:  'D:\\ide_mine\\changing\\'
        :param base: 'ut1_7floorwithWin'
        :param wwrs: [0.1, 0.15, 0.2, 0.25, 0.3]
        :return computational: a list of dicts - wwr_ratio, total_time, simu_time
                bld_dicts: a list of dicts - wwr_ratio, building (object)
        Then the computational list of dicts are returned
        """
        computational = []
        bld_dicts = []
        for wwr in wwrs:
            dict,bld = self.simulation_path(folder, base, wwr)
            if dict:
                computational.append(dict)
                bld_dicts.append(bld)
            time.sleep(2)

        return computational, bld_dicts

    # Run a branch of simulations according to wwrs
    def sequantial_w_html(self, folder, base, wwrs):
        """

        :param folder:
        :param base:
        :param wwrs: a list of wwrs to form simulation paths
        :return:
        """
        computational = []
        html_dicts = []
        for wwr in wwrs:
            dict,bld = self.simulation_path_w_html(folder, base, wwr)
            if dict:
                computational.append(dict)
                html_dicts.append(bld)
            time.sleep(2)

        return computational, html_dicts



    def computational_anls(self, computational):
        """

        :param computational: list of dicts
        :return:
        """
        df = pd.DataFrame(computational)
        df = df.sort_values(by=['wwr_ratio'])

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df["wwr_ratio"], y=df["total_time"],
                                 #                     mode='lines',
                                 name='Total time'))
        fig.add_trace(go.Scatter(x=df["wwr_ratio"], y=df["simu_time"],
                                 #                     mode='lines',
                                 name='Simulation time'))

        fig.show()




class TestSimulation:
    def testOneSimu(self):
        folder = 'D:\\ide_mine\\changing\\'
        model = 'ut1_7floorwithWin_wwr0.2'
        idm = '.idm'
        path = folder+model+idm
        building, pid = connectIDA(path)
        simulate = Simulation()
        res1,res2,res3 = simulate.simulation_bld(building, path)

    def testComputational(self):
        computational = []
        computational.append({'wwr_ratio': 0.1, 'total_time': 274.8782720565796, 'simu_time': 234.21225500106812})
        computational.append({'wwr_ratio': 0.2, 'total_time': 275.2745244503021, 'simu_time': 237.71506309509277})
        computational.append({'wwr_ratio': 0.3, 'total_time': 282.6419041156769, 'simu_time': 247.83287835121155})
        computational.append({'wwr_ratio': 0.05, 'total_time': 258.96157598495483, 'simu_time': 224.94810485839844})

        simulate = Simulation()
        simulate.computational_anls(computational)

    def testSeqSimuWithComp(self):
        folder = 'D:\\ide_mine\\changing\\'
        wwrs = [0.1, 0.15, 0.2, 0.25, 0.3]
        base_model = 'ut1_7floorwithWin'
        simulate = Simulation()
        computational = simulate.seqSimu(folder,base_model,wwrs)
        simulate.computational_anls(computational)







if __name__ == "__main__":
    test1 = TestSimulation()
    test1.testOneSimu()
    # test1.testComputational()
    # test1.testSeqSimuWithComp()