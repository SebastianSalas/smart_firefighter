import numpy as np
import breadth_search as amplitud
import depth_search as profundidad
import cost_search as costo_uniforme
import A_star

class writeMap:
    with open("../resources/map.txt", "r") as file:
      file_map = file.readlines()

      map = np.array([list(map(int, n.split(' '))) for n in file_map])
      expanded_nodes, path, depth, cost, tiempo = A_star.solve(map)
      
      print(f"expanded_nodes: {expanded_nodes}, path: {path}, depth: {depth}, costo: {cost}, tiempo: {tiempo}")
      
