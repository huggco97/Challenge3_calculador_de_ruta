class Nodo:
    def __init__(self, padre = None, posicion = None):
        self.padre = padre
        self.posicion = posicion
        self.g = 0 #coste desde el inicio hasta este nodo
        self.h = 0 #estimacion del coste desde este nodo hasta el objetivo
        self.f = 0 #coste total

def A_estrella(laberinto, inicio, fin):
    # crear nodo inicial y nodo final
    nodo_inicio = Nodo(None, inicio)
    nodo_fin = Nodo(None, fin)

    # inicializar lista open y closed
    open_list = []
    closed_list = []

    # anhadir el nodo inicial a la open_list
    open_list.append(nodo_inicio)

    # Bucle hasta encontrar el objetivo
    while open_list:
        # Obtener el nodo actual
        nodo_actual = open_list[0]
        indice_actual = 0
        for index, item in enumerate(open_list):
            if item.f < nodo_actual.f:
                nodo_actual = item
                indice_actual = index

        # Eliminar nodo actual de open_list y añadirlo a closed_list
        open_list.pop(indice_actual)
        closed_list.append(nodo_actual)

        # Verificar si se ha llegado al nodo objetivo
        if nodo_actual.posicion == nodo_fin.posicion:
            camino = []
            nodo_actual_temp = nodo_actual
            while nodo_actual_temp is not None:
                camino.append(nodo_actual_temp.posicion)
                nodo_actual_temp = nodo_actual_temp.padre
            return camino[::-1]  # Devolver el camino invertido

        # Generar nodos hijos
        hijos = []
        for nueva_posicion in [(0, -1), (0, 1), (-1, 0), (1, 0)]:  # Vecinos
            # Obtener la posición del nodo
            posicion_nodo = (nodo_actual.posicion[0] + nueva_posicion[0], nodo_actual.posicion[1] + nueva_posicion[1])

            # Verificar si está dentro del laberinto
            if posicion_nodo[0] > (len(laberinto) - 1) or posicion_nodo[0] < 0 or posicion_nodo[1] > (len(laberinto[len(laberinto)-1]) - 1) or posicion_nodo[1] < 0:
                continue

            # Verificar si no es un obstáculo
            if laberinto[posicion_nodo[0]][posicion_nodo[1]] != 0:
                continue

            # Crear nuevo nodo
            nuevo_nodo = Nodo(nodo_actual, posicion_nodo)
            hijos.append(nuevo_nodo)

        # Loop a través de hijos
        for hijo in hijos:
            # Si el hijo está en closed_list, saltarlo
            if hijo in closed_list:
                continue

            # Calcular f, g y h
            hijo.g = nodo_actual.g + 1
            hijo.h = ((hijo.posicion[0] - nodo_fin.posicion[0]) ** 2) + ((hijo.posicion[1] - nodo_fin.posicion[1]) ** 2)
            hijo.f = hijo.g + hijo.h

            # Si el hijo está en open_list con menor valor de g, saltarlo
            if any(hijo.posicion == nodo_open.posicion and hijo.g > nodo_open.g for nodo_open in open_list):
                continue

            # Añadir el hijo a open_list
            open_list.append(hijo)
    

laberinto = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 0, 0, 1, 0, 0, 0, 1, 0, 0],
    [2, 0, 0, 1, 0, 1, 0, 0, 0, 2],
    [3, 1, 0, 0, 0, 1, 1, 0, 1, 0],
    [4, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [5, 1, 0, 0, 0, 0, 0, 0, 0, 0], 
    [6, 1, 0, 1, 0, 0, 1, 1, 0, 2],
    [7, 0, 2, 1, 0, 3, 0, 0, 0, 0],
    [8, 1, 0, 0, 0, 3, 0, 0, 2, 0],
    [9, 0, 1, 1, 0, 0, 0, 0, 0, 0]
]

def solicitar_coordenadas(tipo):
    while True:
        coordenadas = tuple(map(int, input(f"Introduce las coordenadas de {tipo} (En este formato: x,y): ").split(",")))
        x, y = coordenadas
        if laberinto[x][y] == 0:
            return coordenadas
        else:
            print(f"La coordenada de {tipo} no es valida, la coordenada ingresada ya esta ocupada. Intentalo de nuevo por favor. ")

#Solicitar coordenada de inicio
inicio = solicitar_coordenadas("inicio")
print(f"Coordenada de inicio aceptada: {inicio}")

#Solicitar coordenada de final
fin = solicitar_coordenadas("fin")
print(f"Coordenada de fin aceptadas: {fin}")

#Solicitar coordenada de obstaculo
obstaculo = solicitar_coordenadas("obstaculo")
print(f"Coordena de obstaculo aceptada: {obstaculo}")
laberinto[obstaculo[0]][obstaculo[1]] = 3

camino = A_estrella(laberinto, inicio, fin)
print("Camino encontrado:", camino)

# guardar camino
for i in range(len(camino)):
    x,y = camino[i][0],camino[i][1]
    laberinto[x][y]='*'

# Marcar el inicio y el fin en el laberinto
laberinto[inicio[0]][inicio[1]] = 'I'
laberinto[fin[0]][fin[1]] = 'F'


for i, fila in enumerate(laberinto):
        
        
        for j, columna in enumerate(fila):
            
        
            if i == 0 or j == 0:
                if(j==0):
                    print(f'\033[32m{columna}\033[0m  ', end=' ')
                else:    
                    print(f'\033[32m{columna}\033[0m', end=' ')
                
                if(i==0 and j==9):
                    print()
                    
            elif laberinto[i][j]==1:
                print(f'\033[31m{columna}\033[0m', end=' ')
            elif laberinto[i][j]=='*':         # El * indica el recorrido elegido como el mas optimo, y lo imprime en amarillo
                print(f'\033[33m{columna}\033[0m', end=' ')
            elif laberinto[i][j]== 3:         # El 3 es un obstaculo mas, se imprime en magenta
                print(f'\033[34m{columna}\033[0m', end=' ')
            elif laberinto[i][j]== 2:         # El 2 indica otro obstaculo, se imprime en celeste
                print(f'\033[36m{columna}\033[0m', end=' ')        
            elif laberinto[i][j]=='I' or laberinto[i][j]=='F': # La I es el Inicio y la F es el final
                print(f'\033[35m{columna}\033[0m', end=' ')
                
                
            else:
                print(columna, end=' ')
        print()