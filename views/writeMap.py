import numpy as np
import algoritmos.amplitud as amplitud

class writeMap:
    with open("resources/map.txt", "r") as file:
      file_map = file.readlines()

      map = np.array([list(map(int, n.split(' '))) for n in file_map])
      amplitud.amplitud(map)
      