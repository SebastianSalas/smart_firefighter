import copy
# Costo para cada suministro
costo_general = 1
cubeta_un_litro = 1 + costo_general
cubeta_dos_litro = 2 + costo_general


class Nodo():

    # define el nodo con los siguientes atributos: padre, posicion, mapa, cubetas, punto_fuego y costo
    def __init__(self, padre, posicion, mapa, cubetas, punto_fuego, costo=0):
        self.padre = padre
        self.posicion = posicion
        self.mapa = mapa
        self.cubetas = cubetas
        self.punto_fuego = punto_fuego
        self.costo = costo


class costo_uniforme():

    # define costo uniforme como algortimo de busqueda

    def __init__(self, mapa):
        self.map = mapa
        
    def movimiento_valido(self, new_x, new_y, nuevo_mapa):
        """
        Verifica si un movimiento a las coordenadas (new_x, new_y) es válido en el mapa n_mapa.
        Debe devolver True si el movimiento es válido y False si no lo es.
        """
        return (0 <= new_x < len(nuevo_mapa)) and (0 <= new_y < len(nuevo_mapa[0])) and nuevo_mapa[new_x][new_y] != 1
    
    def nueva_posicion(self, nodo, direccion):
        """
        Calcula las nuevas coordenadas (new_x, new_y) en función de la dirección.
        Devuelve las coordenadas (new_x, new_y).
        """
        x, y = nodo.posicion

        if direccion == 'up':
            new_x, new_y = x - 1, y
        elif direccion == 'down':
            new_x, new_y = x + 1, y
        elif direccion == 'left':
            new_x, new_y = x, y - 1
        elif direccion == 'right':
            new_x, new_y = x, y + 1
        else:
            raise ValueError("Dirección no válida")

        return new_x, new_y
    # genera nodos hijos a partir de un nodo, o sea expande el nodo

    def expandir_nodos(self, nodo, mapa):
        nuevo_mapa = copy.deepcopy(mapa)
        nodos_hijos = []
        for direccion in ['up', 'down', 'right', 'left']:
            if self.estado_padre(nodo, direccion):
                new_x, new_y = self.nueva_posicion(nodo, direccion)
            if self.movimiento_valido(new_x, new_y, nuevo_mapa):
                nodos_hijos.append(self.state(nodo, new_x, new_y))
        return nodos_hijos
    
    def nodos_vecinos(self, nodo, n_mapa):
        x, y = nodo.posicion
        neighbors = []
        directions = ['up', 'down', 'right', 'left']
        for direction in directions:
            new_x, new_y = self.nueva_posicion(nodo, direction)
        if self.movimiento_valido(new_x, new_y, n_mapa) and self.estado_padre(nodo, direction):
            child = self.state(nodo, new_x, new_y)
            neighbors.append(child)
        return neighbors
    def estado_padre(self, node, direccion):
        if node.padre is None:
            return True
    
        parent_x, parent_y = node.padre.posicion
        padre_cubetas, padre_fuego = node.padre.cubetas, node.padre.punto_fuego
        x, y = node.posicion

        if direccion == 'up' and parent_x == x - 1:
            return not (padre_cubetas == node.cubetas and padre_fuego == node.punto_fuego)
        if direccion == 'down' and parent_x == x + 1:
            return not (padre_cubetas == node.cubetas and padre_fuego == node.punto_fuego)
        if direccion == 'left' and parent_y == y - 1:
            return not (padre_cubetas == node.cubetas and padre_fuego == node.punto_fuego)
        if direccion == 'right' and parent_y == y + 1:
            return not (padre_cubetas == node.cubetas and padre_fuego == node.punto_fuego)
        return True
    def state(self, node, position_x, position_y):
        
        map = copy.deepcopy(node.mapa)
        tipo_celda = map[position_x][position_y]
        cost = costo_general

        if tipo_celda == 3:  # freezer
            cost += cubeta_un_litro if node.seeds == 0 else costo_general
        elif tipo_celda == 4:  # cell
            cost += cubeta_dos_litro if node.seeds == 0 else costo_general

        map[position_x][position_y] = 0
        child = Nodo(node, (position_x, position_y), map, node.seeds, node.spheres, node.cost + cost)

        if tipo_celda == 5:  # seed
            child.seeds += 1
        elif tipo_celda == 6:  # sphere
            child.spheres += 1

        return child
