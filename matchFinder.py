from Matching import Matching
from LCS import LCS

def matchFinderLCS(colVals, clusterIndex) -> list[Matching]:
    matchings = []
    colValsTokens = []
    for value in colVals:
        value = str(value)
        if not isinstance(value, str):
            continue
        
        colValsTokens.append(value.split())
    
    for i in range(len(colValsTokens)):
        for j in range(i, len(colValsTokens)):
            scolValsTokens1 = colValsTokens[i] #sorted(colValsTokens[i], key = len)
            scolValsTokens2 = colValsTokens[j] #sorted(colValsTokens[j], key = len)
            t1 = [[token, 0] for token in scolValsTokens1]
            t2 = [[token, 0] for token in scolValsTokens2]
            
            if len(t1) > len(t2):
                tmp = t1.copy()
                t1 = t2.copy()
                t2 = tmp
            
            if t1 == t2:
                continue
            
            t1 = list(reversed(t1))
            for k in range(len(t1)):
                token1 = t1[k]
                
                matchToken = ["", 0]
                for l in range(len(t2)):
                    if t2[l][1] == -1:
                        continue
                    
                    token2 = t2[l]
                    
                    if token1[0] == token2[0]:
                        token1[1] = -1
                        token2[1] = -1
                        continue
                
                if token1[1] == -1:
                    continue
                
                for l in range(len(t2)):
                    if t2[l][1] == -1:
                        continue
                    
                    token2 = t2[l]
                    
                    _, _, LCS_len = LCS(token1[0], token2[0])
                    if LCS_len == 0:
                        continue
                    if LCS_len > token1[1]:
                        matchToken = [token2[0], l]
                        token1[1] = LCS_len
                        continue
                    
                    if LCS_len == token1[1]:
                        if len(matchToken[0]) > len(token2[0]):
                            matchToken = [token2[0], l]
                
                if len(token1[0]) > len(matchToken[0]):
                    matchings.append(Matching(token1[0], matchToken[0], token1[1], clusterIndex, i, j, k, matchToken[1]))
                else:
                    matchings.append(Matching(matchToken[0], token1[0], token1[1], clusterIndex, j, i, matchToken[1], k))
    return matchings
                        
def matchFinderCell(colVals) -> list[Matching]:
    matchings = []
    valueList = []
    for value in colVals:
        value = str(value)
        valueList.append(value)
    
    for i in range(len(valueList)):
        for j in range(i, len(valueList)):
            if valueList[i] == valueList[j]:
                continue
            matchings.append(Matching(valueList[i], valueList[j], LCS(valueList[i], valueList[j]), 0, 0, 0, 0, 0))
    
    return matchings
                    
                
                    
            
            
            
            