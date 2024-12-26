import simpy
import random


class Puerto:
    def __init__(self, env, nombre, num_cajeros, num_gruas, num_controladores):
        self.env = env
        self.nombre = nombre
        self.cajero = simpy.Resource(env, num_cajeros)
        self.grua = simpy.Resource(env, num_gruas)
        self.controlador = simpy.Resource(env, num_controladores)

    def gestionar_atraque(self, barco):
        # Tiempo de llegada al puerto
        tiempo_llegada = self.env.now
        print(f"{barco.nombre} ha llegado para atracar en {self.nombre} a las {tiempo_llegada}")
        
        # Pago de tarifas portuarias
        with self.cajero.request() as solicitud:
            yield solicitud
            print(f"{barco.nombre} está pagando tarifas en {self.nombre} a las {self.env.now}")
            yield self.env.timeout(random.randint(1, 3))

        # Revisión de documentación
        with self.controlador.request() as solicitud:
            yield solicitud
            print(f"{barco.nombre} está en revisión de documentación en {self.nombre} a las {self.env.now}")
            yield self.env.timeout(1)

        # Carga o descarga si se requiere
        if random.choice([True, False]):
            with self.grua.request() as solicitud:
                yield solicitud
                print(f"{barco.nombre} comienza carga/descarga en {self.nombre} a las {self.env.now}")
                yield self.env.timeout(random.randint(1, 5))


class Ruta:
    def __init__(self, puerto_inicio, puerto_destino, duracion):
        self.puerto_inicio = puerto_inicio
        self.puerto_destino = puerto_destino
        self.duracion = duracion

    def viajar(self, env, barco):
        # Simula el viaje entre el puerto de inicio y el puerto de destino
        print(f"{barco.nombre} comienza su viaje de {self.puerto_inicio.nombre} a {self.puerto_destino.nombre} a las {env.now}")
        yield env.timeout(self.duracion)
        print(f"{barco.nombre} llega a {self.puerto_destino.nombre} a las {env.now}")
        yield env.process(self.puerto_destino.gestionar_atraque(barco))


class Barco:
    def __init__(self, env, nombre, ruta):
        self.env = env
        self.nombre = nombre
        self.ruta = ruta

    def iniciar_viaje(self):
        # Inicia el viaje en la ruta especificada
        yield self.env.process(self.ruta.viajar(self.env, self))


def simulacion(env):
    # Puertos
    puerto_a = Puerto(env, "Puerto A", num_cajeros=1, num_gruas=2, num_controladores=1)
    puerto_b = Puerto(env, "Puerto B", num_cajeros=1, num_gruas=2, num_controladores=1)

    # Rutas entre puertos
    ruta_a_b = Ruta(puerto_inicio=puerto_a, puerto_destino=puerto_b, duracion=5)
    ruta_b_a = Ruta(puerto_inicio=puerto_b, puerto_destino=puerto_a, duracion=7)

    # Barcos que viajan en rutas específicas
    for i in range(10):
        barco = Barco(env, f"Barco {i}", ruta_a_b if i % 2 == 0 else ruta_b_a)
        env.process(barco.iniciar_viaje())

# Simulación
env = simpy.Environment()
simulacion(env)
env.run(until=20)
