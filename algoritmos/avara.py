import numpy as np
from node_informed_search import Node
from collections import deque
    
def heuristic_fun(nodo, water_positions, fire_positions, bucket_positions):
    # Calcular la distancia al punto de agua más cercano
        closest_water = min([((nodo.position[0] - water[0]) ** 2 + (nodo.position[1] - water[1]) ** 2) ** 0.5 for water in water_positions])
    # Calcular la distancia al punto de fuego más cercano
        closest_fire = min([((nodo.position[0] - fire[0]) ** 2 + (nodo.position[1] - fire[1]) ** 2) ** 0.5 for fire in fire_positions])
    # Calcular la distancia a la cubeta más cercana
        closest_bucket = min([((nodo.position[0] - bucket[0]) ** 2 + (nodo.position[1] - bucket[1]) ** 2) ** 0.5 for bucket in bucket_positions])
    # Sumar las distancias calculadas para obtener la heurística
        return closest_water + closest_fire + closest_bucket

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
def selectNode(nodes_list):
  return min(nodes_list, key=lambda nodo: nodo.heuristic)
def verifyNodeBranchCicle(nodo, next_pos):
    current_nod = nodo
    while current_nod.parent is not None and not current_nod.change_state:
        if current_nod.position == next_pos:
            return False
        current_nod = current_nod.parent
    return True

def checkParent(nodo, operator):
    if nodo.parent is None:
        return True

    if operator == 0:  # up
        if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
            return verifyNodeBranchCicle(nodo, [nodo.position[0] - 1, nodo.position[1]])
    elif operator == 1:  # down
        if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
            return verifyNodeBranchCicle(nodo, [nodo.position[0] + 1, nodo.position[1]])
    elif operator == 2:  # right
        if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
            return verifyNodeBranchCicle(nodo, [nodo.position[0], nodo.position[1] + 1])
    elif operator == 3:  # left
        if nodo.parent.bucket1 == nodo.bucket1 and nodo.parent.bucket2 == nodo.bucket2 and nodo.parent.fire_extinguished == nodo.fire_extinguished and nodo.parent.water_q == nodo.water_q:
            return verifyNodeBranchCicle(nodo, [nodo.position[0], nodo.position[1] - 1])

    return True

def checkMovimiento(nodo, nodos_e,fire_positions, water_positions,bucket_positions):
    child_list = []
    pos_x = nodo.position[0]
    pos_y = nodo.position[1]
    expanded_nodes = nodos_e
    heuristic_value = heuristic_fun(nodo,water_positions, fire_positions,bucket_positions)

    if verifyMap(nodo, [pos_x, pos_y+1]) and checkParent(nodo, 2):
        child, expanded_nodes = verifyGoal(nodo, pos_x, pos_y+1, nodos_e, 2)
        child.heuristic = heuristic_value  # Asigna la heurística calculada
        child_list.append(child)
    if verifyMap(nodo, [pos_x-1, pos_y]) and checkParent(nodo, 0):
        child, expanded_nodes = verifyGoal(nodo, pos_x-1, pos_y, nodos_e, 0)
        child.heuristic = heuristic_value  # Asigna la heurística calculada
        child_list.append(child)
    if verifyMap(nodo, [pos_x+1, pos_y]) and checkParent(nodo, 1):
        child, expanded_nodes = verifyGoal(nodo, pos_x+1, pos_y, nodos_e, 1)
        child.heuristic = heuristic_value  # Asigna la heurística calculada
        child_list.append(child)
    if verifyMap(nodo, [pos_x, pos_y-1]) and checkParent(nodo, 3):
        child, expanded_nodes = verifyGoal(nodo, pos_x, pos_y-1, nodos_e, 3)
        child.heuristic = heuristic_value  # Asigna la heurística calculada
        child_list.append(child)

    return child_list, expanded_nodes

def verifyGoal(nodo, pos_x, pos_y, nodos_e, operator):
    expanded_nodes = nodos_e
    water_temp = nodo.water_q
    nodo_map = (nodo.map).copy()
    if nodo_map[nodo.position[0], nodo.position[1]] == 3:
        new_map = np.where(np.logical_or(
        nodo_map == 3, nodo_map == 4), 0, nodo_map)
        node_child = Node(nodo, operator, [pos_x, pos_y], new_map, True, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1, True)
        expanded_nodes += 1
    elif nodo_map[nodo.position[0], nodo.position[1]] == 4:
        new_map = np.where(np.logical_or(
            nodo_map == 3, nodo_map == 4), 0, nodo_map)
        node_child = Node(nodo, operator, [pos_x, pos_y], new_map, nodo.bucket1, True, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1, True)
        expanded_nodes += 1
    elif nodo_map[nodo.position[0], nodo.position[1]] == 2:
        if nodo.bucket1 and water_temp > 0:
            nodo_map[nodo.position[0], nodo.position[1]] = 0
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished + 1, nodo.water_q - 1, nodo.depth + 1, True)
            expanded_nodes += 1
        elif nodo.bucket2 and water_temp > 0:
            nodo_map[nodo.position[0], nodo.position[1]] = 0
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished + 1, nodo.water_q - 1, nodo.depth + 1, True)
            expanded_nodes += 1
        else:
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1, False)
            expanded_nodes += 1
    elif nodo_map[nodo.position[0], nodo.position[1]] == 6:
        if nodo.bucket1 and nodo.water_q == 0:
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1,
                      nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 1, nodo.depth + 1, True)
            expanded_nodes += 1
        elif nodo.bucket2 and nodo.water_q == 0:
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q + 2, nodo.depth + 1, True)
            expanded_nodes += 1
        else:
            node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1, False)
            expanded_nodes += 1
    else:
        node_child = Node(nodo, operator, [pos_x, pos_y], nodo_map, nodo.bucket1, nodo.bucket2, nodo.fire_extinguished, nodo.water_q, nodo.depth + 1, False)
        expanded_nodes += 1

    return node_child, expanded_nodes

def solve(map):
    stack = deque()
    children_nodes = []
    finished = False
    expanded_nodes = 0
    pos_i = []

    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if (map[i][j] == 5):
                pos_i = [i, j]

    nodo_i = Node(None, None, pos_i, map, False, False, 0, 0, 0, False,0,0)
    stack.append(nodo_i)
    #count_fire = np.count_nonzero(map == 2)
    
    fire_positions = [[4,3],[5,7]]
    bucket_positions = [[1,7],[5,5]]
    water_position=[[4,5]]
    
    while not finished:
        current_node = selectNode(stack)
        stack.remove(current_node)
        
        if current_node.fire_extinguished == len(fire_positions):
            finished = True
        else:
            children_nodes, expanded_nodes = checkMovimiento(current_node, expanded_nodes, water_position, fire_positions,bucket_positions)
            stack.extendleft(reversed(children_nodes))

    path = []
    list_heu = []
    depth = current_node.depth
    heuris = current_node.heuristic
    while current_node.parent is not None:
        path.append(current_node.operator)
        list_heu.append(current_node.heuristic)
        current_node = current_node.parent
        
    path.append(current_node.operator)
    list_heu.append(current_node.operator)
    path = path[::-1]
    list_heu = list_heu[::-1]
    cost = current_node.cost

    return expanded_nodes, path, depth,heuris,list_heu,cost

# Prueba del algoritmo
map = np.array([
    [0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 0, 1, 1, 1, 1],
    [0, 1, 0, 2, 0, 0, 0, 0, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 0],
    [5, 0, 0, 6, 4, 0, 0, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 0, 1, 0, 1],
    [3, 0, 0, 0, 2, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 0, 0, 0, 0, 0, 1, 0, 1],
    [0, 1, 0, 1, 1, 1, 0, 0, 0, 0]
])

expanded_nodes, path, depth,heuris,list_heu,cost = solve(map)
print("Número de nodos expandidos:", expanded_nodes)
print("Camino encontrado:", path)
print("Profundidad del camino:", depth)
print("Heuristicas: ",list_heu)
print("Costo:", cost)