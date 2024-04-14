import heapq
from sklearn.cluster import KMeans
import numpy as np

class Estacion:
    def __init__(self, nombre):
        self.nombre = nombre
        self.vecinos = {}  # Diccionario de estaciones vecinas y tiempo de viaje

    def agregar_vecino(self, estacion, tiempo):
        self.vecinos[estacion] = tiempo

    def __hash__(self):
        return hash(self.nombre)

    def __eq__(self, otro):
        return isinstance(otro, Estacion) and self.nombre == otro.nombre

def encontrar_ruta(estacion_inicial, estacion_objetivo):
    nodo_inicial = Nodo(estacion_inicial)
    nodo_objetivo = Nodo(estacion_objetivo)
    
    nodos_explorados = []
    heapq.heappush(nodos_explorados, nodo_inicial)
    nodos_visitados = set()

    while nodos_explorados:
        nodo_actual = heapq.heappop(nodos_explorados)

        if nodo_actual.estado == estacion_objetivo:
            # Reconstruir la ruta
            ruta = []
            tiempo_total = 0
            while nodo_actual:
                ruta.append(nodo_actual.estado.nombre)
                if nodo_actual.padre:
                    tiempo_total += nodo_actual.estado.vecinos[nodo_actual.padre.estado]
                nodo_actual = nodo_actual.padre
            return ruta[::-1], tiempo_total

        if nodo_actual.estado in nodos_visitados:
            continue

        nodos_visitados.add(nodo_actual.estado)

        for estacion_vecina, tiempo in nodo_actual.estado.vecinos.items():
            if estacion_vecina not in nodos_visitados:
                nuevo_costo = nodo_actual.costo + tiempo
                nuevo_nodo = Nodo(estacion_vecina, nodo_actual, nuevo_costo)
                heapq.heappush(nodos_explorados, nuevo_nodo)

    return None, None

class Nodo:
    def __init__(self, estado, padre=None, costo=0):
        self.estado = estado
        self.padre = padre
        self.costo = costo

    def __lt__(self, otro):
        return (self.costo) < (otro.costo)

# Crear estaciones
estaciones = {
    1: Estacion(1),
    2: Estacion(2),
    3: Estacion(3),
    4: Estacion(4),
    5: Estacion(5),
    6: Estacion(6)
}

# Establecer conexiones entre estaciones y tiempos de viaje
estaciones[1].agregar_vecino(estaciones[2], 5)
estaciones[1].agregar_vecino(estaciones[3], 10)
estaciones[1].agregar_vecino(estaciones[4], 8)
estaciones[1].agregar_vecino(estaciones[5], 12)

estaciones[2].agregar_vecino(estaciones[1], 5)
estaciones[2].agregar_vecino(estaciones[3], 3)
estaciones[2].agregar_vecino(estaciones[6], 7)

estaciones[3].agregar_vecino(estaciones[1], 10)
estaciones[3].agregar_vecino(estaciones[2], 3)

estaciones[4].agregar_vecino(estaciones[1], 8)

estaciones[5].agregar_vecino(estaciones[1], 12)

estaciones[6].agregar_vecino(estaciones[2], 7)


# Solicitar al usuario la estación de origen y destino
while True:
    origen = int(input("Ingrese el número de la estación de origen (1, 2, 3, 4, 5, 6): "))
    if origen in estaciones:
        break
    else:
        print("Estación de origen no válida. Intente nuevamente.")

while True:
    destino = int(input("Ingrese el número de la estación de destino (1, 2, 3, 4, 5, 6): "))
    if destino in estaciones:
        break
    else:
        print("Estación de destino no válida. Intente nuevamente.")

# Encontrar la ruta óptima
ruta_optima, tiempo_total = encontrar_ruta(estaciones[origen], estaciones[destino])

if ruta_optima:
    print("Ruta óptima encontrada:", ruta_optima)
    print("Tiempo total de viaje:", tiempo_total, "minutos")
else:
    print("No se pudo encontrar una ruta.")

# Obtener los datos de las estaciones y sus conexiones como una matriz numpy
datos_estaciones = []
max_vecinos = max(len(estacion.vecinos) for estacion in estaciones.values())
for estacion in estaciones.values():
    vecinos = list(estacion.vecinos.values())
    vecinos.extend([0] * (max_vecinos - len(vecinos)))  # Rellenar con ceros si es necesario
    datos_estaciones.append(vecinos)
datos_estaciones = np.array(datos_estaciones)

# Configurar y entrenar el modelo K-Means
k = 3  # Número de clusters deseado
modelo = KMeans(n_clusters=k)
modelo.fit(datos_estaciones)

# Obtener las etiquetas de cluster asignadas a cada estación
etiquetas_clusters = modelo.labels_

# Imprimir las estaciones y sus respectivas etiquetas de cluster
print("Estación\tCluster")
for i, estacion in enumerate(estaciones.values()):
    print(estacion.nombre, "\t\t", etiquetas_clusters[i])