from Structs import *

def aggregateByStrucs(transforms : list[Transformation]):
    groups = {}
    
    for t in transforms:
        if t.symbol not in groups.keys():
            groups[t.symbol] = [t]
            continue
        
        groups[t.symbol].append(t)
    
    return groups