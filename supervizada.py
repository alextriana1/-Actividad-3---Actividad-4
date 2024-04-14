import heapq
import pandas as pd


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


# Función para encontrar el tiempo de viaje entre dos estaciones vecinas
def tiempo_entre_estaciones(estacion_origen, estacion_destino):
    return estacion_origen.vecinos.get(estacion_destino, float('inf'))

# Crear una lista de todas las combinaciones posibles de estaciones vecinas
combinaciones_estaciones_vecinas = [(i, j) for i in estaciones.values() for j in estaciones.values() if i != j and j in i.vecinos]

# Generar datos de tiempo de viaje para cada combinación de estaciones vecinas
datos_tiempo_viaje = []
for origen, destino in combinaciones_estaciones_vecinas:
    tiempo_viaje = tiempo_entre_estaciones(origen, destino)
    datos_tiempo_viaje.append({
        'Estacion_origen': origen.nombre,
        'Estacion_destino': destino.nombre,
        'Tiempo_viaje': tiempo_viaje
    })

# Convertir los datos a un DataFrame de pandas
df_tiempo_viaje = pd.DataFrame(datos_tiempo_viaje)

# Mostrar los primeros registros del DataFrame
print(df_tiempo_viaje.head())
