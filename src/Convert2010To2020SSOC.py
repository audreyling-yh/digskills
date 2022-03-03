import pandas as pd


class Convert2010To2020SSOC:
    def __init__(self, frameworks_path, output_path):
        self.frameworks_path = frameworks_path
        self.output_path = output_path

    def run(self):
        print('Compiling SSOC 2010 to 2020 mapping')

        mapping = self.convert_2010_to_2018()
        mapping = self.convert_2018_to_2020(mapping)

        mapping.to_csv(self.output_path, index=False)

    def convert_2010_to_2018(self):
        # map 2010 SSOC to 2015 (v2018)
        filepath = self.frameworks_path.format('DOS/ssoc2015-2010ct', 'xls')
        map1015 = pd.read_excel(filepath)[['SSOC 2010', 'SSOC 2015', 'SSOC 2010 Description']]
        map1015 = map1015[map1015['SSOC 2010']!='new item']

        filepath = self.frameworks_path.format('DOS/ssoc2015v2018ssoc2015ctr', 'xls')
        map1518 = pd.read_excel(filepath, skiprows=4)[['SSOC 2015', 'SSOC 2015\n(Version 2018)']]

        mapping = map1015.merge(map1518, on=['SSOC 2015'], how='left')
        mapping.rename(columns={'SSOC 2015\n(Version 2018)': 'SSOC 2015 (Version 2018)'}, inplace=True)

        return mapping

    def convert_2018_to_2020(self, mapping):
        # map 2015 (v2018) SSOC to 2020
        filepath = self.frameworks_path.format('DOS/Correspondence Tables between SSOC2020 and 2015v18', 'xlsx')
        map1820 = pd.read_excel(filepath, skiprows=4)[['SSOC 2020', 'SSOC 2015 (Version 2018)', 'SSOC 2020 Title']]

        mapping = mapping.merge(map1820, on=['SSOC 2015 (Version 2018)'], how='left')

        return mapping
