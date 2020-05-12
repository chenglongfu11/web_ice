from util import *
from basic import *
from bs4 import BeautifulSoup
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os.path
from os import path

"""
        Generate html reports -> Retrieve Energy Grand Total (kwh, kwh/m2) and form dataframes -> plot dataframes
"""

class Readhtml:
    def genehtml_bld(self, building, folder, filename):
        """
            Given building object, output the file
                path = D:\\ide_mine\\changing\\
                filename=ut1_7floorwithWin_wwr0.25
        """

        energy_report = ida_get_named_child(building, 'ENERGY-REPORT')
        html_path = folder + filename + '.html'
        res = call_ida_api_function(ida_lib.printReport, energy_report, html_path.encode(), 1)
        time.sleep(2)
        a = path.exists(html_path)
        if not a:
            print('Fail to generate the html report from ', filename)
            return False
        else:
            print('Generated the html report in ', html_path)
            return html_path


    def genehtml_path(self, folder, base, wwr):
        idm = '.idm'

        file_path = folder + base + '_wwr' + str(wwr) + idm

        building = connectIDA2(file_path)
        html_path = self.genehtml_bld(building, folder, base+'_wwr'+str(wwr))
        return  html_path


    def multi_gene_html(self, folder, base, wwrs):
        """

        :param folder:
        :param base:
        :param wwrs:
        :return: a list of html paths
        """
        html_ls = []
        for wwr in wwrs:
            res = self.genehtml_path(folder, base, wwr)
            if res:
                html_ls.append(res)

        return html_ls


    def multi_gene_html_blds(self, blds, folder, base):
        """
        :param blds: a list of dicts - building objects, wwr_ratio
        :param folder: target folder
        :param filename: target filename
        :return: a list of dicts -html, wwr
        """
        html_dict_ls = []
        for bld in blds:
            building = blds['building']
            wwr = blds['wwr_ratio']
            html_res = self.genehtml_bld(building, folder, base + '_wwr' + str(wwr))
            if html_res:
                dict = {'html': html_res, 'wwr_ratio':wwr}
                html_dict_ls.append(dict)

        return html_dict_ls


    # Retrieve grand total from beautifulSoup
    def grand_total(self, html_path):
        htmlfile = open(html_path, 'r', encoding='utf-8')
        htmlhandle = htmlfile.read()

        # soup
        soup = BeautifulSoup(htmlhandle, 'lxml')

        tds = soup.findAll('td')
        result = {}
        for i in range(len(tds)):
            if 'Grand total' in tds[i].get_text():
                result['kwh'] = float(tds[i + 1].get_text())
                result['kwhm2'] = float(tds[i + 2].get_text())

        return result


    # Retrieve grand total from dataframe
    def grand_total_df(self, df):
        a = df.loc[df['facility'] == 'Grand total']
        return a


    def deliverd_energy_df(self, path, wwr):
        """
        df[0].columns
        MultiIndex([('Unnamed: 0_level_0', 'Unnamed: 0_level_1'),
            ('Unnamed: 1_level_0', 'Unnamed: 1_level_1'),
            (  'Purchased energy',                'kWh'),
            (  'Purchased energy',         'kWh/m2  kW'),
            (       'Peak demand', 'Unnamed: 4_level_1')],
           )


        :param path:
        :return: dataframe of delived enegy overview
        """
        try:
            htmlfile = open(path, 'r', encoding='utf-8')
            htmlhandle = htmlfile.read()
        except:
            print('Missing html file of', path)
            return pd.Series([])

        # soup
        soup = BeautifulSoup(htmlhandle, 'lxml')

        tables = soup.findAll("table")
        table = tables[2]    # Normally, Delivered Energy Overview is the third table
        df = pd.read_html(str(table))
        df = df[0]
        df.columns = [' '.join(col).strip() for col in df.columns.values]  # MultiIndex to SingleIndex
        df.columns = ['wwr_ratio', 'facility', 'kwh', 'kwh/m2', 'kw']

        for rindex in df.index:
            df.loc[rindex, 'wwr_ratio'] = wwr

        return df



    def multi_df_html(self, html_dict_ls):
        """

        :param html_dict_ls: a list of dicts: html, wwr_ratio
        :return: list of dataframes
        """
        dfs= []
        for path in html_dict_ls:
            html_path = path['html']
            wwr = path['wwr_ratio']
            df_res = self.deliverd_energy_df(html_path, wwr)
            if not df_res.empty:
                dfs.append(df_res)

        return dfs




    def multi_df_wwr(self, folder, base, wwrs):
        """
         Combine several dataframes from several generated html files
        :param folder: 'D:\\ide_mine\\changing\\'
        :param base: 'ut1_7floorwithWin'
        :param wwrs: [0.1, 0.15, 0.2, 0.25, 0.3]
        :return: list of dataframes
        """
        htm = '.html'
        dfs = []
        for wwr in wwrs:
            html_path = folder + base + '_wwr' + str(wwr) + htm
            df_res = self.deliverd_energy_df(html_path, wwr)
            if not df_res.empty:
                dfs.append(df_res)

        return dfs



    def parametric_anls(self, dfs):
        """

        :param dfs: list of dataframe
        :return:
        """
        df_tot = pd.concat(dfs, axis=0)

        subdf = df_tot[df_tot['facility'] == 'Grand total']
        subdf = subdf.sort_values(by=['wwr_ratio'])


        fig = make_subplots(rows=1, cols=2)
        fig.add_trace(go.Scatter(x=subdf["wwr_ratio"], y=subdf["kwh"],
                                 #                     mode='lines',
                                 name='kWh'),row=1, col=1)
        fig.add_trace(go.Scatter(x=subdf["wwr_ratio"], y=subdf["kwh/m2"],
                                 #                     mode='lines',
                                 name='kWh/m2'), row = 1, col =2)

        fig.show()






class TestReadHtml:
    def testGene(self):
        readHTML = Readhtml()
        wwrList = ['wwr0.1', 'wwr0.2', 'wwr0.3', 'wwr0.15', 'wwr0.25']
        folder = 'D:\\ide_mine\\changing\\'
        base_model = 'ut1_7floorwithWin'
        idm = '.idm'

        for wwr in wwrList:
            file_path = folder+base_model+'_'+wwr+idm
            print(file_path)
            building = connectIDA2(file_path)
            html_path = readHTML.genehtml(building, folder, base_model+'_'+wwr)


    def testDf(self):
        wwrs = [0.1, 0.15, 0.2, 0.25, 0.3]
        folder = 'D:\\ide_mine\\changing\\'
        base_model = 'ut1_7floorwithWin'

        readHTML = Readhtml()
        # Generate html reports for list of wwrs
        html_ls = readHTML.multi_gene_html(folder, base_model, wwrs)
        # Retrieve the dataframe of deliverd energy
        dfs = readHTML.multi_df_wwr(folder, base_model, wwrs)
        readHTML.parametric_anls(dfs)









if __name__ == "__main__":
    test1 = TestReadHtml()
    test1.testDf()



