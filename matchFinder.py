from Matching import Matching
from LCS import LCS

def matchFinderLCS(colVals : list[str]) -> list[Matching]:
    matchings = []
    colValsTokens = []
    for value in colVals:
        colValsTokens.append(str(value).split())
    
    for i in range(len(colValsTokens)):
        for j in range(i, len(colValsTokens)):
            scolValsTokens1 = sorted(colValsTokens[i], key = len)
            scolValsTokens2 = sorted(colValsTokens[j], key = len)
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
                
                matchToken = ""
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
                        matchToken = token2[0]
                        token1[1] = LCS_len
                        continue
                    
                    if LCS_len == token1[1]:
                        if len(matchToken) > len(token2[0]):
                            matchToken = token2[0]
                
                matchings.append(Matching(token1[0], matchToken, token1[1]))
    return matchings
                        
                        
                    
                
                    
            
            
            
            