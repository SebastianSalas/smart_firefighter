import numpy as np
import amplitud as amplitud
import profundidad 
import costo_uniforme

class writeMap:
    with open("../resources/map.txt", "r") as file:
      file_map = file.readlines()

      map = np.array([list(map(int, n.split(' '))) for n in file_map])
      expanded_nodes, path, depth, cost, list_cost = costo_uniforme.solve(map)
      
      print(f"expanded_nodes: {expanded_nodes}, path: {path}, depth: {depth}, costo: {list_cost}")
      