from prepData import *
from aggregating import *
from matchFinder import *
import pandas as pd
from datetime import datetime
from tqdm import tqdm
class GoldenFinder:
    def __init__(self, df):
        self.df = df.reset_index()
        self.clusters = None
        self.matchings = None
        self.groups = None
        self.matchCol = None
        self.uniqueCol = None
        self.dateCol = None
        self.uniquedf = None
        
    def getClusters(self, uniqueCol : str, matchCol : str):
        self.uniqueCol = uniqueCol
        self.matchCol = matchCol
        self.clusters, unique_values = dubl(self.df, uniqueCol, matchCol)
        self.uniquedf = self.df[self.df[uniqueCol].isin(unique_values)]
        
    def getMatchings(self, mode : str):
        self.matchings = []
        for i in range(len(self.clusters)):
            if mode == "LCS":
                self.matchings.extend(matchFinderLCS(self.clusters[self.matchCol].iloc(i), i))
            if mode == "Cell":
                self.matchings.extend(matchFinderCell(self.clusters[self.matchCol].iloc(i)))
            
    def getTransformations(self):
        self.transformations = [Transformation(m) for m in self.matchings]
        
    def getGroups(self, mode : str):
        if mode == 'Struct':
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
        self.dateCol = dateCol

        # Генерация словаря индекс-кластер на основе self.clusters
        index_to_cluster = {
            i: cluster_id 
            for cluster_id, indices in self.clusters['index'].items() 
            for i in indices
        }

        # Создание нового столбца в self.df с идентификатором кластера
        self.df['cluster_id'] = self.df.index.map(index_to_cluster)

        # Группировка по идентификатору кластера и выбор строки с наибольшей датой
        # Сначала сортируем, затем выбираем последнюю строку в каждой группе
        result_df = (
            self.df.sort_values(by=[dateCol]).groupby('cluster_id', as_index=False).last()
        )

        print(len(self.clusters.index))
        result_df_cutted = result_df.loc[:, result_df.columns.isin(self.uniquedf.columns)]

        # Возвращаем результат
        return pd.concat([result_df_cutted, result_df], ignore_index=True)
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
