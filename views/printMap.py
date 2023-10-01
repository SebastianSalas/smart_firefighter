import numpy as np

class writeMap:
    with open("resources/map.txt", "r") as file:
      file_map = file.readlines()

      map = np.array([list(map(int, n.split(' '))) for n in file_map])
      print(map[0][1])