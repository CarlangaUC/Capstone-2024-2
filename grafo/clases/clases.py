from itertools import cycle
import numpy as np
import simpy

UNIT_TIME = 1


class Ship:
    ship_id = 0

    def __init__(self, env, name, speed, port_id, cycles,recharge,itinerary):
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
        #Tiempo de carga y descarga y metemos el itinerario de barcos como interno en simpy
        self.recharge = recharge 
        self.itinerary = itinerary
        self.actual_port = port_id
        
    def unload(self,archivo):
        # simula la descarga del barco, espera según la carga que tiene
        #archivo.write(f"Barco {self.ship_id} descargando...\n")
        archivo.write(f"event;ES2;{self.ship_id};{self.actual_port};{self.env.now}\n")
        yield self.env.timeout(self.recharge)

    def drive(self, final_port, dist, route_id,archivo): #Metodo importante, pensar sobrecarga de puertos y cambio de rutas
        # seteamos la carga
        # movemos el barco
        while self.pos < dist:
            #archivo.write(f"{self.name}, ruta {route_id}, posicion: {self.pos}, "
                #f"tiempo simulacion {self.env.now}\n")
            self.pos += self.speed
            pos_total = round(self.pos/dist,2)
            #Escribir output formato
            archivo.write(f"event;ES1;{self.ship_id};{self.actual_port}-{final_port.port_id};{pos_total};{self.env.now}\n")
            yield self.env.timeout(UNIT_TIME)
        # estacionamos en el puerto, esperando si es necesario
        with final_port.resource.request() as request:
            # este yield es para que la simulación espere
            # hasta que el recurso se libere
            yield request
            self.pos = 0
            final_port.ships.append(self.ship_id)
            # al hacer yield del proceso esperamos a que
            # la función unload termine
            yield self.env.process(self.unload(archivo))
            final_port.ships.remove(self.ship_id)


class Port:

    def __init__(self, env, name, capacity, port_id):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.port_id = port_id
        self.ships = []
        self.resource = simpy.Resource(env, capacity=capacity)


class Route:

    def __init__(self, env, initial_port_id, final_port_id, dist):
        self.env = env
        self.initial_port_id = initial_port_id
        self.final_port_id = final_port_id
        self.dist = dist
        # creamos el id de esta forma para después hacer la
        # búsqueda de una ruta más rápida
        self.route_id = f"{initial_port_id}-{final_port_id}"
        self.ships = []


class Manager:

    def __init__(self):
        self.env = simpy.Environment()
        self.ships = {}
        self.ports = {}
        self.routes = {}
        self.archivo = open("archivo.txt","w")
                
    # representa el event loop para un barco en particular 
    def ship_event_loop(self, ship, events,archivo):
        actual_port_id = ship.port_id
        # si cicla, entonces cambiamos events por cycle(events),
        # que nos entrega una generador que repite los elementos
        # de events infinitamente
        events = ship.itinerary
        
        if ship.cycles:
            events = cycle(events)
        for final_port_id in events:
            final_port = self.ports[final_port_id]
            route = self.routes[f"{actual_port_id}-{final_port_id}"]
            route.ships.append(ship.ship_id)
            # al hacer yield del proceso esperamos a que
            # la función drive termine
            yield self.env.process(ship.drive(final_port,route.dist, route.route_id,archivo))
            route.ships.remove(ship.ship_id)
            actual_port_id = final_port_id
            ship.actual_port = final_port_id

    def processes(self):
        #Procesar cada barco con su itinerario asociado
        for ship_id, ship in self.ships.items():
            self.env.process(self.ship_event_loop(ship,ship.itinerary,self.archivo))
            

    def run(self, until):
        self.env.run(until=until)

    # estas funciones generator son solo una forma "elegante" de cargar los
    # .txt como instancias. NO tienen que ver con la simulación en simpy y
    # no son tan importantes.
    def ports_generator(self, ports_file):
        with open(ports_file) as file:
            file.readline()
            for line in file:
                data = line.strip().split(";")
                yield Port(self.env, data[0],
                           int(data[1]), int(data[2]))

    def routes_generator(self, routes_file):
        with open(routes_file) as file:
            file.readline()
            for line in file:
                data = line.strip().split(";")
                yield Route(self.env, int(data[0]),
                            int(data[1]), int(data[2]))

    def ships_generator(self, ships_file):
        with open(ships_file) as file:
            file.readline()  
            for line in file:
                data = line.strip().split(";")
                name = data[0]
                speed = float(data[1])
                port_id = int(data[2])
                cycles = int(data[3])
                recharge = int(data[4])  
                itinerary = list(map(int, data[5].split(",")))  
                yield Ship(self.env, name, speed, port_id, cycles, recharge, itinerary)

    def add_ports(self, ports_file):
        for i, port in enumerate(self.ports_generator(ports_file)):
            self.ports[port.port_id] = port
        self.matrix = -1 * np.ones((i + 1, i + 1))

    def add_routes(self, routes_file):
        for route in self.routes_generator(routes_file):
            self.routes[route.route_id] = route
            self.matrix[route.initial_port_id][route.final_port_id] = route.dist

    def add_ships(self, ships_file):
        for ship in self.ships_generator(ships_file):
            self.ships[ship.ship_id] = ship

    def add(self, ports_file, routes_file, ships_file):
        self.add_ports(ports_file)
        self.add_routes(routes_file)
        self.add_ships(ships_file)
        self.output(self.archivo)

    #Formar formato pedido
    def output(self,archivo):
        
        for ship in self.ships.values():
            archivo.write(f"ship;{ship.ship_id};{ship.name};{ship.itinerary[0]};{ship.speed};0.0\n")
            
        for port in self.ports.values():
            
            archivo.write(f"port;{port.port_id};{port.name}\n")
            
        for rout in self.routes.values():
            
            archivo.write(f"route;{rout.initial_port_id}-{rout.final_port_id};1\n")
            
        
#este evento es el de recorrer, lo metere en el input a cada uno, adapta la parte de leer barcos con esto en mente