import simpy
import math

# La idea de este modelo simple es simular tres puertos con barcos, donde
# cada barco tiene puertos de origen y destino a los que va de ida y vuelta.
# La idea es simular tanto el viaje entre puertos como procesos de carga y
# descarga. Otra idea es la de simular capacidad de los puertos (lo cual
# está también en el archivo main)

# Cree esta función de distancia euclidiana entre puertos
def distancia(puerto_origen, puerto_destino):
    x1, y1 = puerto_origen.coordenadas
    x2, y2 = puerto_destino.coordenadas
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Aquí definí clases de Puerto y Barco
class Puerto:
    def __init__(self, nombre, coordenadas, capacidad_maxima):
        self.nombre = nombre
        self.coordenadas = coordenadas
        self.capacidad_maxima = capacidad_maxima
        self.barcos_actuales = 0
    
    # Definimos estas funciones para ver si el Puerto puede o no recibir barcos
    # Se lleva un conteo de los barcos en cada puerto
    def puede_recibir(self):
        return self.barcos_actuales < self.capacidad_maxima

    def recibir_barco(self):
        if self.puede_recibir():
            self.barcos_actuales += 1
            return True
        else:
            return False

    def liberar_barco(self):
        if self.barcos_actuales > 0:
            self.barcos_actuales -= 1

class Barco:
    def __init__(self, env, nombre, puerto_origen, puerto_destino, tiempo_carga, tiempo_descarga, velocidad):
        self.env = env
        self.nombre = nombre
        self.puerto_origen = puerto_origen
        self.puerto_destino = puerto_destino
        self.tiempo_carga = tiempo_carga
        self.tiempo_descarga = tiempo_descarga
        self.velocidad = velocidad
        self.accion = env.process(self.viajar())

    def viajar(self):
        while True:
            # Se carga en el puerto de origen
            print(f'{self.nombre} está cargando en {self.puerto_origen.nombre} en t={self.env.now}')
            yield self.env.timeout(self.tiempo_carga)

            # Se ve si es que es posible recibir al barco en el puerto de destino
            if self.puerto_destino.puede_recibir():
                # Se viaja si es que es posible
                distancia_a_recorrer = distancia(self.puerto_origen, self.puerto_destino)
                tiempo_viaje = distancia_a_recorrer / self.velocidad
                print(f'{self.nombre} está viajando de {self.puerto_origen.nombre} a {self.puerto_destino.nombre} (distancia: {distancia_a_recorrer:.2f}) en t={self.env.now}')
                yield self.env.timeout(tiempo_viaje)

                # Se descarga en el puerto de destino
                self.puerto_destino.recibir_barco()
                self.puerto_origen.liberar_barco()
                print(f'{self.nombre} está descargando en {self.puerto_destino.nombre} en t={self.env.now}')
                yield self.env.timeout(self.tiempo_descarga)

                # Finalmente, se invierten los papeles. Se cambia puerto de origen con el de destino (se invierten)
                self.puerto_origen, self.puerto_destino = self.puerto_destino, self.puerto_origen
            else:
                # Si no se puede, se escribe un mensaje y se espera un tiempo
                print(f'{self.nombre} no puede dirigirse a {self.puerto_destino.nombre} porque está lleno en t={self.env.now}')
                yield self.env.timeout(1)

# Aqui creamos la simulación
env = simpy.Environment()
puerto_A = Puerto('A', (0, 0), capacidad_maxima=2)
puerto_B = Puerto('B', (10, 0), capacidad_maxima=1)
puerto_C = Puerto('C', (5, 10), capacidad_maxima=2)
barco_1 = Barco(env, 'Barco 1', puerto_A, puerto_B, tiempo_carga=5, tiempo_descarga=3, velocidad=2)
barco_2 = Barco(env, 'Barco 2', puerto_B, puerto_C, tiempo_carga=4, tiempo_descarga=3, velocidad=2)
barco_3 = Barco(env, 'Barco 3', puerto_C, puerto_A, tiempo_carga=6, tiempo_descarga=2, velocidad=2)
env.run(until=50)
