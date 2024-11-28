class Matching:
    def __init__(self, a : str, b : str, p : int, cluster_index : int, a_str_index : int, b_str_index : int, a_index : int, b_index : int):
        self.a = a
        self.b = b
        self.priority = p
        self.b_str_index = b_str_index
        self.a_str_index = a_str_index
        self.a_index = a_index
        self.b_index = b_index
        self.cluster_index = cluster_index
        
        