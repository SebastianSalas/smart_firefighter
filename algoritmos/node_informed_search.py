class Node():
    """
    Represents a node in a search algorithm.
    """
    def __init__(self, parent, operator, position, map, bucket1, bucket2, fire_extinguished, water_q, depth, cost=0,heuristic=0):
        """
        Initializes a new instance of the Node class
        """
        self.parent = parent
        self.operator = operator
        self.position = position
        self.map = map
        self.bucket1 = bucket1
        self.bucket2 = bucket2
        self.fire_extinguished = fire_extinguished
        self.water_q = water_q
        self.depth = depth
        self.cost = cost
        self.heuristic = heuristic