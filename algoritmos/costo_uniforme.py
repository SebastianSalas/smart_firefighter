def movimientos(x,y,punto_fuego,cubeta_agua,estado_agente,mapa,costo_agente,copy_mapa,hidratante):
    final = []
    e_agente=estado_agente
    PuntoFuego=punto_fuego
    nueva_matriz=copy_mapa
    costo=0
    costo_2=0
    cuebtas=cubeta_agua
    agente=costo_agente
    
    if (mapa[y, x] == 0):
        costo += 1
        costo_2 = costo + agente[-1]
        agente[0] = costo_2
        
    if (mapa[y, x] == 2):
        PuntoFuego[0] += 1
        nueva_matriz[y, x] = 0
        if (PuntoFuego[0] == 1):
            e_agente[1] = [x, y]
        if (PuntoFuego[0] == 2):
            e_agente[2] = [x, y]
        costo += 1
        costo_2 = costo + agente[-1]
        agente[0] = costo_2
    
    if (mapa[y, x] == 3):
        nueva_matriz[y, x] = 0
        costo += 2
        costo_2 = costo + agente[-1]
        agente[0] = costo_2
        cubeta_agua[0] += 1
        if ([(x, y)] not in e_agente[3]):
            if (cubeta_agua[0] >= 1):
                e_agente[3] = [[x, y]]