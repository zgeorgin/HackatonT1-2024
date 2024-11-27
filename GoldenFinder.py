from prepData import *
from aggregating import *
from matchFinder import matchFinderLCS
import pandas as pd

class GoldenFinder:
    def __init__(self, df):
        self.df = df
        self.clusters = None
        self.matchings = None
        
    def getClusters(self, uniqueCol : str):
        self.clusters = dubl(self.df, uniqueCol)
        
    def getMatchings(self, matchCol : str, mode : str):
        self.matchings = []
        for i in range(len(self.clusters)):
            if mode == "LCS":
                self.matchings.extend(matchFinderLCS(self.clusters[i][matchCol]))
            
    def getTransformations(self):
        self.transformations = [Transformation(m) for m in self.matchings]
        
    def getGroups(self, mode : str):
        if mode == 'Structs':
            self.groups = aggregateByStrucs(self.transformations)
    
        
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