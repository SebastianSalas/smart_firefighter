from collections import deque
import numpy as np
from NodeNotInformedSearch import Node
  
def verifyMap(nodo, position):
    if 0 <= position[0] < nodo.map.shape[0] and 0 <= position[1] < nodo.map.shape[1] and nodo.map[position[0], position[1]] != 1:
      if nodo.map[position[0], position[1]] == 2:
        if (nodo.bucket1 or nodo.bucket2) and nodo.water_q != 0:
          return True
        else:
          return False
      else:
        return True
    else:
      return False

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
  
    
def checkMovimiento(nodo, nodos_e):
  child_list = []
  pos_x = nodo.position[0]
  pos_y = nodo.position[1]
  expanded_nodes = nodos_e
  
  # right
  if verifyMap(nodo,[pos_x, pos_y+1]) and checkParent(nodo, 2):
    child, expanded_nodes = verifyGoal(nodo, pos_x, pos_y+1, nodos_e, 2)
    child_list.append(child)
  # up
  if verifyMap(nodo,[pos_x-1, pos_y]) and checkParent(nodo, 0):
    child, expanded_nodes = verifyGoal(nodo, pos_x-1, pos_y, nodos_e, 0)
    child_list.append(child)
  # down
  if verifyMap(nodo,[pos_x+1, pos_y]) and checkParent(nodo, 1):
    child, expanded_nodes = verifyGoal(nodo, pos_x+1, pos_y, nodos_e, 1)
    child_list.append(child)
  # left
  if verifyMap(nodo,[pos_x, pos_y-1]) and checkParent(nodo, 3):
    child, expanded_nodes = verifyGoal(nodo, pos_x, pos_y-1, nodos_e, 3)
    child_list.append(child)

  return child_list, expanded_nodes  
    

def verifyGoal(nodo, pos_x, pos_y, nodos_e, operator):
  expanded_nodes = nodos_e
  water_temp = nodo.water_q
  nodo_map = (nodo.map).copy()
  if nodo_map[nodo.position[0], nodo.position[1]] == 3: #1l
    new_map = np.where(np.logical_or(nodo_map == 3, nodo_map == 4), 0, nodo_map)
    node_child = Node(nodo, operator, [pos_x, pos_y], new_map, True, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1)
    expanded_nodes += 1
  elif nodo_map[nodo.position[0], nodo.position[1]] == 4: #2l
    new_map = np.where(np.logical_or(nodo_map == 3, nodo_map == 4), 0, nodo_map)
    node_child = Node(nodo, operator, [pos_x, pos_y], new_map, nodo.bucket1, True, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1)
    expanded_nodes += 1
  elif nodo_map[nodo.position[0], nodo.position[1]] == 2: #fire
    if nodo.bucket1 and water_temp > 0: 
      nodo_map[nodo.position[0], nodo.position[1]] = 0
      node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished + 1, nodo.water_q - 1, nodo.depth + 1)
      expanded_nodes += 1
    elif nodo.bucket2 and water_temp > 0:
      nodo_map[nodo.position[0], nodo.position[1]] = 0
      node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished + 1, nodo.water_q - 1, nodo.depth + 1)
      expanded_nodes += 1
    else:
      node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1)
      expanded_nodes += 1
  elif nodo_map[nodo.position[0], nodo.position[1]] == 6: #water
    if nodo.bucket1 and nodo.water_q == 0:
        node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 1, nodo.depth + 1)
        expanded_nodes += 1
    elif nodo.bucket2 and nodo.water_q == 0:
        node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 2, nodo.depth + 1)
        expanded_nodes += 1
    else:
      node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1)
      expanded_nodes += 1
  else:
    node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1)
    expanded_nodes += 1
    
  return node_child, expanded_nodes

    

def solve(map):
  queue = deque()
  children_nodes = []
  finished = False
  expanded_nodes = 0
  pos_i = []
 
  
  #Posición inicial del bombero
  for i in range(map.shape[0]):  # filas
      for j in range(map.shape[1]): #columnas
        if(map[i][j] == 5):
          pos_i= [i,j]
          
  nodo_i = Node(None, None, pos_i, map, False, False, 0, 0, 0)
  queue.append(nodo_i)
  count_fire = np.count_nonzero(map == 2)
  while not finished:
    current_node = queue.popleft()
    if current_node.fire_extinguished == count_fire:
      finished = True
    else:
      children_nodes, expanded_nodes = checkMovimiento(current_node, expanded_nodes)
      queue.extend(children_nodes)
  
  path = []
  depth = current_node.depth
  while current_node.parent is not None:
      path.append(current_node.operator) 
      current_node = current_node.parent  

  path.append(current_node.operator)

  path = path[::-1]

  return expanded_nodes, path, depth


      
 