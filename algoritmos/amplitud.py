from collections import deque

def verificarNodoVisitado(map,nodos):
  for i in range(map.shape[0]):  # filas
      for j in range(map.shape[1]): #columnas
        return [i,j] in nodos
  
def verificarDentroDelMapa(nodo, map):
  return 0 <= nodo[0] < map.shape[0] and 0 <= nodo[1] < map.shape[1]
    
def retornarHijos(nodo_padre,map):
  lista_hijos=[]
  for n in list(([nodo_padre[0]+1,nodo_padre[1]], [nodo_padre[0]-1,nodo_padre[1]], [nodo_padre[0],nodo_padre[1]+1], [nodo_padre[0],nodo_padre[1]-1])):
          if verificarDentroDelMapa(n,map):
            lista_hijos.append(n)
  return lista_hijos

def amplitud(map):
  nodos_visitados = deque()
  nodos_hijos = []
  
  for i in range(map.shape[0]):  # filas
    for j in range(map.shape[1]): #columnas
      if(map[i][j] == 5):
        nodos_visitados.append([i,j])
        nodos_hijos = retornarHijos([i,j], map)
        
        
      
  print(nodos_hijos)