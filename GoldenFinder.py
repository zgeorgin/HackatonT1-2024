from prepData import *
from aggregating import *
from matchFinder import *
import pandas as pd

class GoldenFinder:
    def __init__(self, df):
        self.df = df.reset_index()
        self.clusters = None
        self.matchings = None
        self.groups = None
        self.matchCol = None
        self.uniqueCol = None
        self.dateCol = None
        
    def getClusters(self, uniqueCol : str, matchCol : str):
        self.uniqueCol = uniqueCol
        self.matchCol = matchCol
        self.clusters = dubl(self.df, uniqueCol, matchCol)
        
    def getMatchings(self, mode : str):
        self.matchings = []
        for i in range(len(self.clusters)):
            if mode == "LCS":
                self.matchings.extend(matchFinderLCS(self.clusters[self.matchCol][i], i))
            if mode == "Cell":
                self.matchings.extend(matchFinderCell(self.clusters[self.matchCol][i]))
            
    def getTransformations(self):
        self.transformations = [Transformation(m) for m in self.matchings]
        
    def getGroups(self, mode : str):
        if mode == 'Structs':
            self.groups = aggregateByStrucs(self.transformations)
    
    def applyGroup(self, groupIndex : int):
        for t in self.groups[list(self.groups.items())[groupIndex][0]]:
            a_index = t.m.a_index
            b_index = t.m.b_index
            cluster_index = t.m.cluster_index
            #print(self.clusters[self.matchCol][cluster_index], t.m.a, t.m.b)
            #print("AAAAAAAAAAAA")
            a_str = (str(self.clusters[self.matchCol][cluster_index][t.m.a_str_index])).split()
            b_str = (str(self.clusters[self.matchCol][cluster_index][t.m.b_str_index])).split()
            #print(a_str, b_str, a_index, b_index, cluster_index, t.m.a, t.m.b)
            if (a_index < len(a_str)) and (b_index < len(b_str)) and (a_str[a_index] == t.m.a) and (b_str[b_index] == t.m.b):
                a_str[a_index] = t.m.b
                self.clusters[self.matchCol][cluster_index][t.m.a_str_index] = ' '.join(a_str)
                print(self.clusters[self.matchCol][cluster_index][t.m.a_str_index])
    
    def applyClusters(self):
        for index, row in self.clusters.iterrows():
            for value1, value2, idx in zip(row[self.uniqueCol], row[self.matchCol], row['index']):
                self.df.loc[idx, self.uniqueCol] = value1
                self.df.loc[idx, self.matchCol] = value2
    
    def getGolden(self, dateCol):
        result_df = pd.DataFrame()
        self.dateCol = dateCol
        for index, row in self.clusters.iterrows():
            indicies = row['index']
            rows = self.df.loc[indicies]
            
            latest_row = rows.loc[rows[self.dateCol]]
            for column in latest_row.index:
                if pd.isna(latest_row[column]):
                    non_nan_value = rows[column].dropna().values
                    if non_nan_value.size > 0:
                        latest_row[column] = non_nan_value[0]
        
            result_df = result_df.append(latest_row, ignore_index=True)

'''
Example:

uniqueCol = "client_id" 
matchCol = "client_fio_full"

GF = GoldenFinder(pd.read_csv("ds_dirty_fin_202410041147.csv"))

GF.getClusters(uniqueCol)
GF.getMatchings(matchCol, "LCS")

GF.getTransformations()
GF.getGroups("Structs")

print(GF.clusters[1]["client_fio_full"].values())
print(GF.groups)
GF.groups['TETeT-TETe -> TCT-TC'][0].print()
'''