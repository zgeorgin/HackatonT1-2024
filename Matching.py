class Matching:
    def __init__(self, a : str, b : str, p : int, cluster_index : int, a_index : int, a_str : int):
        self.a = a
        self.b = b
        self.priority = p
        self.a_str = a_str
        self.a_index = a_index
        self.cluster_index = cluster_index
        
        