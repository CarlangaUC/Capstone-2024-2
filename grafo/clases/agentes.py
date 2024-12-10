import simpy
import random

UNIT_TIME = 1
WEATHER_FACT = 1
SECURITY_FACT = 1
REGULATIONS_FACT = 1

class Ship:
    ship_id = 0

    def __init__(self, env, name, speed, port_id,
                 cycles, recharge, itinerary):
        self.env = env
        self.name = name
        self.speed = speed
        self.port_id = port_id
        self.ship_id = Ship.ship_id
        self.load = 0
        self.pos = 0
        # True si su itinerario es cíclico, sino False
        self.cycles = bool(cycles)
        self.route_id = ""
        Ship.ship_id += 1
        # Tiempo de carga y descarga y metemos el itinerario
        # de barcos como interno en simpy
        self.recharge_ = recharge
        self.itinerary = itinerary
        self.actual_port = port_id

    
        #Metricas
        
        #Tiempo total del itinerario
        self.start_time = 0
        self.end_time = 0

        #Tiempo de espera en rutas y puertos
        self.total_wait_time_routes = 0
        self.total_wait_time_ports = 0

    @property
    def recharge(self):
        # usamos una distributción uniforme entre recharge_ (tiempo mínimo de
        # recarga) y recharge_ más 10
        return int(random.randint(self.recharge_, self.recharge_ + 10))

    def unload(self, archivo):
        # simula la descarga del barco, espera según la carga que tiene
        archivo.write(f"event;ES2;{self.ship_id};{self.actual_port};"
                      f"{self.env.now}\n")
        print(f"Barco {self.ship_id} descargando...")
        yield self.env.timeout(self.recharge)

# Método importante, pensar sobrecarga de puertos y cambio de rutas

    def drive(self, final_port, route, archivo, matriz_adyacencia):
        # Recurso compartido, no es necesario preguntarse si cierra/capacidad
        # llena a mitad del viaje dado que lo parte estando lleno
        
        #PENSAR SI SE TIENE QUE ESPERAR A LOS DEMAS BARCOS PARA OCUPARLA
        
        
        with route.resource.request() as request:
            
            print(f"{self.name} esperando...")
            wait_start = self.env.now
            yield request
            
            self.total_wait_time_routes += self.env.now - wait_start
            
            
            while self.pos < route.dist:
                self.pos += self.speed
                pos_total = round(self.pos/route.dist, 2)
                # Escribir output formato
                archivo.write(f"event;ES1;{self.ship_id};{self.actual_port}-"
                              f"{final_port.port_id};{pos_total};"
                              f"{self.env.now}\n")
                print(f"{self.name}, ruta {route.route_id}, "
                      f"posicion: {self.pos}, "
                      f"tiempo simulacion {self.env.now}")
                
                yield self.env.timeout(UNIT_TIME)
                
        with final_port.resource.request() as request:
            
            print(f"{self.name} esperando...")
            wait_start = self.env.now            
            yield request
            
            self.total_wait_time_ports += self.env.now - wait_start 

            self.pos = 0
            final_port.ships.append(self.ship_id)
            # al hacer yield del proceso esperamos a que
            # la función unload termine
            # MATAR Y VERIFICAR SI ESTA ABIERTO NUEVAMENTE
            yield self.env.process(self.unload(archivo))
            final_port.ships.remove(self.ship_id)
            

class Port:

    def __init__(self, env, name, capacity, port_id):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.port_id = port_id
        self.ships = []
        self.open = True  # ASUMIR QUE TODOS PARTEN ABIERTOS
        self.resource = simpy.Resource(env, capacity=capacity)


class Route:

    def __init__(self, env, initial_port_id, final_port_id,
                 dist, capacity, weather, security, regulations):
        self.env = env
        self.initial_port_id = initial_port_id
        self.final_port_id = final_port_id
        self.dist = dist
        
        self.weather = weather
        self.security = security
        self.regulations = regulations
        
        # creamos el id de esta forma para después hacer la
        # búsqueda de una ruta más rápida
        
        self.route_id = f"{initial_port_id}-{final_port_id}"
        self.ships = []
        self.resource = simpy.Resource(env, capacity=capacity)
        self.open = True

