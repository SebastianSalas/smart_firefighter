from collections import deque
import numpy as np

class Node():
    '''
    Clase que define un nodo.
    '''
    def __init__(self, parent, operator, position, map, bucket1, bucket2, fire_extinguished, water_q, cost=0):
      self.parent = parent
      self.operator = operator
      self.position = position
      self.map = map
      self.bucket1 = bucket1
      self.bucket2 = bucket2
      self.fire_extinguished = fire_extinguished
      self.water_q = water_q
      self.cost = cost
      
    def update_fire_extinguished(self):
      self.fire_extinguished += 1
  
def verificarCaminoMapa(nodo, map):
  return 0 <= nodo[0] < map.shape[0] and 0 <= nodo[1] < map.shape[1] and map[nodo[0], nodo[1]] != 1

def checkParent(nodo, operator):
  if nodo.parent == None:
    return True
  
  if operator == 0: #up
    if nodo.parent.position == [nodo.position[0] - 1, nodo.position[1]]:
      if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
        return False
      else:
        return True    
  elif operator == 1: #down
    if nodo.parent.position == [nodo.position[0] + 1, nodo.position[1]]:
      if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
        return False
      else:
        return True
  elif operator == 2: #right
    if nodo.parent.position == [nodo.position[0], nodo.position[1] + 1]:
      if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
        return False
      else:
        return True   
  elif operator == 3: #left
    if nodo.parent.position == [nodo.position[0], nodo.position[1] - 1]:
      if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
        return False
      else:
        return True
      
  return True
  
    
def checkMovimiento(nodo, map, nodos_e):
  child_list=[]
  pos_x = nodo.position[0]
  pos_y = nodo.position[1]
  nodos_expandidos = nodos_e
  #up
  if verificarCaminoMapa([nodo.position[0]-1, nodo.position[1]], map) and checkParent(nodo, 0):
    pos_x = nodo.position[0]-1
    pos_y = nodo.position[1]
    child, nodos_expandidos = verificarMeta(nodo, map, pos_x, pos_y, nodos_e)
    print(f"fuego_child: {child.fire_extinguished}")
    child_list.append(child)
    
  #down
  if verificarCaminoMapa([nodo.position[0]+1, nodo.position[1]], map) and checkParent(nodo, 1):
    pos_x = nodo.position[0]+1
    pos_y = nodo.position[1]
    child, nodos_expandidos = verificarMeta(nodo, map, pos_x, pos_y, nodos_e)
    print(f"fuego_child: {child.fire_extinguished}")
    child_list.append(child)
    
  #right
  if verificarCaminoMapa([nodo.position[0], nodo.position[1]+1], map) and checkParent(nodo, 2):
    pos_x = nodo.position[0]
    pos_y = nodo.position[1]+1
    child, nodos_expandidos = verificarMeta(nodo, map, pos_x, pos_y, nodos_e)
    print(f"fuego_child: {child.fire_extinguished}")
    child_list.append(child)
    
  #left
  if verificarCaminoMapa([nodo.position[0], nodo.position[1]-1], map) and checkParent(nodo, 3):
    pos_x = nodo.position[0]
    pos_y = nodo.position[1]-1
    child, nodos_expandidos = verificarMeta(nodo, map, pos_x, pos_y, nodos_e)
    print(f"fuego_child: {child.fire_extinguished}")
    child_list.append(child)

  return child_list, nodos_expandidos      
    

def verificarMeta(nodo, copyMap, pos_x, pos_y, nodos_e):
  nodos_expandidos = nodos_e
  if copyMap[nodo.position[0], nodo.position[1]] == 3:
    #print(f"Coge el cubo 1L {nodo.position}")
    new_map = np.where(np.logical_or(copyMap == 3, copyMap == 4), 0, copyMap)
    node_child = Node(nodo, 0, [pos_x, pos_y], new_map, True, nodo.bucket2, nodo.fire_extinguished, nodo.water_q)
    nodos_expandidos += 1
  elif copyMap[nodo.position[0], nodo.position[1]] == 4:
    #print(f"Coge cubo de 2L {nodo.position}")
    new_map = np.where(np.logical_or(copyMap == 3, copyMap == 4), 0, copyMap)
    node_child = Node(nodo, 0, [pos_x, pos_y], new_map, nodo.bucket1, True, nodo.fire_extinguished, nodo.water_q)
    nodos_expandidos += 1
  elif copyMap[nodo.position[0], nodo.position[1]] == 2:
    if nodo.bucket1 and nodo.water_q > 0:
      #print(f"Apaga fuego {nodo.position}")
      copyMap[nodo.position[0], nodo.position[1]] = 0
      nodo.update_fire_extinguished()
      node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q - 1)
      #print(f"FUEGOOOOOOOOOOOOOOOOOOOO: {node_child.fire_extinguished}")
      print(f"cubo1l: {nodo.bucket1}, cubo2l: {nodo.bucket2}, fuegos: {nodo.fire_extinguished}, matriz_nuev: {copyMap}")
      nodos_expandidos += 1
    elif nodo.bucket2 and nodo.water_q > 0:
      #print(f"Apaga fuego {nodo.position}")
      copyMap[nodo.position[0], nodo.position[1]] = 0
      nodo.update_fire_extinguished()
      node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q - 1)
      #print(f"FUEGOOOOOOOOOOOOOOOOOOOO: {node_child.fire_extinguished}")
      print(f"cubo1l: {nodo.bucket1}, cubo2l: {nodo.bucket2}, fuegos: {nodo.fire_extinguished}, matriz_nuev: {copyMap}")
      nodos_expandidos += 1
    else:
      #print(f"Sigue el camino {nodo.position}")
      node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q)
      nodos_expandidos += 1
  elif copyMap[nodo.position[0], nodo.position[1]] == 6:
    #print(f"cubeta 1l: {nodo.bucket1}, cubeta 2l: {nodo.bucket2},")
    if nodo.bucket1 and nodo.water_q == 0:
        #print(f"Llena agua 1L {nodo.position}")
        node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 1)
        nodos_expandidos += 1
    elif nodo.bucket2 and nodo.water_q == 0:
        #print(f"Llena agua 2L {nodo.position}")
        node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 1)
        nodos_expandidos += 1
    else:
      #print(f"Sigue el camino {nodo.position}")
      node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q)
      nodos_expandidos += 1
  else:
    #print(f"Sigue el camino {nodo.position}")
    node_child = Node(nodo, 0, [pos_x, pos_y], copyMap, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q)
    nodos_expandidos += 1
    
  return node_child, nodos_expandidos

    

def solve(map):
  cola = deque()
  nodos_hijos = []
  mapa_actual = map.copy()
  finished = False
  nodos_expandidos = 0
  pos_i = []
 
  
  #Posición inicial del bombero
  for i in range(map.shape[0]):  # filas
      for j in range(map.shape[1]): #columnas
        if(map[i][j] == 5):
          pos_i= [i,j]
          
  nodo_i = Node(None, None, pos_i, mapa_actual, False, False, 0, 0)
  cola.append(nodo_i)
  
  while not finished:
    nodo_actual = cola.popleft()
    #print(nodo_actual.fire_extinguished)
    if nodo_actual.fire_extinguished == 2:
      finished = True
    else:
      #print(f"Cola {cola}")
      #print(nodo_actual.position)
      nodos_hijos, nodos_expandidos = checkMovimiento(nodo_actual, nodo_actual.map, nodos_expandidos)
      cola.extend(nodos_hijos)
  print(f"nodos actual: {nodo_actual.position}")
  
  path = []
  while nodo_actual.parent is not None:
      path.append(nodo_actual.position) 
      nodo_actual = nodo_actual.parent  

  path.append(nodo_actual.position)

  path = path[::-1]

  print(path)


      
 