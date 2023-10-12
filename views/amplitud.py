from collections import deque
import numpy as np

class Node():
    '''
    Clase que define un nodo teniendo en cuenta un padre.
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
  
def verificarCaminoMapa(nodo, map):
  return 0 <= nodo[0] < map.shape[0] and 0 <= nodo[1] < map.shape[1] and map[nodo[0], nodo[1]] != 1

def checkParent(nodo, operator):
  if nodo.parent == None:
    return True
  
  if operator == 0: #up
    print(f"parent = {nodo.parent.position } child = {[nodo.position[0] - 1, nodo.position[1]]}")
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
  
    
def retornarHijos(nodo, map, nodos_e):
  lista_hijos=[]
  nodos_expandidos = nodos_e
  #up
  if verificarCaminoMapa([nodo.position[0]-1, nodo.position[1]], map) and checkParent(nodo, 0):
    lista_hijos.append(Node(nodo, 0, [nodo.position[0]-1, nodo.position[1]], nodo.map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q))
    nodos_expandidos +=1
    
  #down
  if verificarCaminoMapa([nodo.position[0]+1, nodo.position[1]], map) and checkParent(nodo, 1):
    lista_hijos.append(Node(nodo, 0, [nodo.position[0]+1, nodo.position[1]], nodo.map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q))
    nodos_expandidos +=1
    
  if verificarCaminoMapa([nodo.position[0], nodo.position[1]+1], map) and checkParent(nodo, 2):
    lista_hijos.append(Node(nodo, 0, [nodo.position[0], nodo.position[1]+1], nodo.map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q))
    nodos_expandidos +=1
    
  if verificarCaminoMapa([nodo.position[0], nodo.position[1]-1], map) and checkParent(nodo, 3):
    lista_hijos.append(Node(nodo, 0, [nodo.position[0], nodo.position[1]-1], nodo.map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q))
    nodos_expandidos +=1
    
  return lista_hijos, nodos_expandidos

def verificarMeta(nodo,copyMap):
  if copyMap[nodo.position[0], nodo.position[1]] == 3:
    print("Coge el cubo 1L")
    copyMap = np.where(np.logical_or(copyMap == 3, copyMap == 4), 0, copyMap)
    nodo.bucket1 = True
  elif copyMap[nodo.position[0], nodo.position[1]] == 4:
    print("Coge cubo de 2L")
    copyMap = np.where(np.logical_or(copyMap == 3, copyMap == 4), 0, copyMap)
    nodo.bucket2 = True
  elif copyMap[nodo.position[0], nodo.position[1]] == 2:
    if(nodo.bucket1 and nodo.water_q):
      print("Apaga fuego")
      nodo.fire_extinguished += 1
      nodo.water_q -= 1
      copyMap[nodo.position[0], nodo.position[1]] = 0
    elif(nodo.bucket2 and nodo.water_q):
      print("Apaga fuego")
      nodo.fire_extinguished += 1
      nodo.water_q -= 1
      copyMap[nodo.position[0], nodo.position[1]] = 0
  elif copyMap[nodo.position[0], nodo.position[1]] == 6:
      if(nodo.bucket1 and nodo.water_q == 0):
        print("Llena agua 1L")
        nodo.water_q += 1
      elif(nodo.bucket2 and nodo.water_q == 0):
        print("Llena agua 2L")
        nodo.water_q += 2
  #print(nodo.position)
  return copyMap  
    

def solve(map):
  nodos_visitados = deque()
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
          nodos_visitados.append([i,j])
          
  nodo_i = Node(None, None, pos_i, mapa_actual, False, False, 0, 0)
  cola.append(nodo_i)
  
  while not finished:
    nodo_actual = cola.popleft()
    nodos_visitados.append(nodo_actual)
    if nodo_actual.fire_extinguished == 2:
      finished = True
    else:
      #print(f"Cola {cola}")
      #print(nodo_actual.position)
      mapa_actual = verificarMeta(nodo_actual,mapa_actual)
      nodos_hijos, nodos_expandidos = retornarHijos(nodo_actual, mapa_actual, nodos_expandidos)
      cola.extend(nodos_hijos)
  print(f"nodos expandidos: {nodos_expandidos}")
      
 