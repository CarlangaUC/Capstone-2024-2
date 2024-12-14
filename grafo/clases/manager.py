from itertools import cycle
from clases.input_auto import generate_agents
from clases.agentes import Ship, Port, Route
import numpy as np
import simpy
import heapq


UNIT_TIME = 1
WEATHER_FACT = 1
SECURITY_FACT = 1
REGULATIONS_FACT = 1
        
        
class Manager:

    def __init__(self):
        self.env = simpy.Environment()
        self.ships = {}
        self.ports = {}
        self.routes = {}
        self.archivo = open("archivo.txt", "w")
        #self.info = {}
        
    # representa el event loop para un barco en particular

        
    def search_route(self, actual_port_id, final_port, matriz_adyacencia):
        
        N = len(matriz_adyacencia)
        costos = [float('inf')] * N
        costos[actual_port_id] = 0
        previos = [-1] * N
        visitados = [False] * N
        cola_prioridad = [(0, actual_port_id)]

        
        while cola_prioridad:
            costo_actual, puerto_actual = heapq.heappop(cola_prioridad)
            if visitados[puerto_actual]:
                continue
            visitados[puerto_actual] = True
            if puerto_actual == final_port:
                break
            for vecino in range(N):
                ruta_id = matriz_adyacencia[puerto_actual][vecino] 
                if ruta_id == 0:
                    continue 
                ruta_temp = self.routes[ruta_id]
                costo_ruta = (
                    ruta_temp.dist
                    + WEATHER_FACT * ruta_temp.weather
                    + SECURITY_FACT * ruta_temp.security
                    + REGULATIONS_FACT * ruta_temp.regulations
                )
                if costo_ruta > 0 and not visitados[vecino]:
                    nuevo_costo = costo_actual + costo_ruta
                    if nuevo_costo < costos[vecino]:
                        costos[vecino] = nuevo_costo
                        previos[vecino] = puerto_actual
                        heapq.heappush(cola_prioridad, (nuevo_costo, vecino))

        if costos[final_port] == float('inf'):
            print("No hay ruta disponible entre los puertos.")
            return None

        # Reconstruir la ruta
        ruta = []
        puerto = final_port
        while puerto != -1 and previos[puerto] != -1:
            ruta.append(f"{previos[puerto]}-{puerto}")
            puerto = previos[puerto]
        ruta.reverse()
        if ruta == []:
            print("No hay ruta disponible entre los puertos.")
            return None
        print("Ruta encontrada:", ruta)
        return ruta


    def ship_event_loop(self, ship, events, archivo):
        actual_port_id = ship.port_id
        events = ship.itinerary  
        test = events
        visitados = set()  
        ship.start_time = self.env.now
        intentos_fallidos = 0  

        while len(visitados) != len(test): 

            #print("Puertos visitados:", visitados)
            #print("Itinerario pendiente:", test)
            
            progreso = False  
            
            for final_port_id in events:
                if final_port_id not in visitados:
                    final_port = self.ports[final_port_id]
                    if not final_port.open:
                        print(f"El puerto {final_port_id} está cerrado.")
                        continue
                    
                    rutas = self.search_route(actual_port_id, final_port_id, self.matrix)
                    if rutas is None:
                        print(f"No hay ruta disponible hacia el puerto {final_port_id}.")
                        continue
                    
                    progreso = True  # Hay una ruta disponible
                    for ruta in rutas:
                        route = self.routes[ruta]
                        route.ships.append(ship.ship_id)
                        try:
                            yield self.env.process(
                                ship.drive(final_port, route, archivo, self.matrix)
                            )
                        except Exception as e:
                            print(f"Error durante el viaje: {e}")
                            route.ships.remove(ship.ship_id)
                            continue
                        route.ships.remove(ship.ship_id)
                        actual_port_id = final_port_id
                        ship.actual_port = final_port_id
                    visitados.add(final_port_id)
            
            # Si no se pudo avanzar en este ciclo
            if not progreso:
                intentos_fallidos += 1
                #print(f"Intento fallido {intentos_fallidos}: no se puede avanzar.")
                
                # Terminar si todos los puertos son inaccesibles
                if intentos_fallidos >= len(events):
                    #print("Todos los puertos son inaccesibles. Terminando itinerario.")
                    ship.end_time = self.env.now
                    return
            
            # Reiniciar el itinerario si es cíclico
            if ship.cycles and len(visitados) == len(test):
                visitados = set()
                ship.end_time = self.env.now  
        
        ship.end_time = self.env.now


        
        
    def processes(self):
        # procesar cada barco con su itinerario asociado
        for ship_id, ship in self.ships.items():
            self.env.process(self.ship_event_loop(ship, ship.itinerary,
                                                  self.archivo))

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
                yield Route(self.env, int(data[0]), int(data[1]),
                            int(data[2]), int(data[3]), float(data[4]), float(data[5]), float(data[6]))

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
                yield Ship(self.env, name, speed, port_id,
                           cycles, recharge, itinerary)

    def add_ports(self, ports_file):
        for i, port in enumerate(self.ports_generator(ports_file)):
            self.ports[port.port_id] = port
            
        #ASUMIR IDS SECUENCIALES PARA QUE NO SE ESCAPE LA MATRIZ DE RANGO
        
        self.matrix = [[0 for _ in range(i + 1)] for _ in range(i + 1)]

    def add_routes(self, routes_file):
        for route in self.routes_generator(routes_file):
            self.routes[route.route_id] = route
            self.matrix[route.initial_port_id][route.final_port_id] = route.route_id
        #print(self.matrix)

    def add_ships(self, ships_file):
        for ship in self.ships_generator(ships_file):
            self.ships[ship.ship_id] = ship

    def add(self, n_ports = None, input_file = None):
        if input_file == None:
            ports,routes,ships,matrix = generate_agents(self.env, n_ports)

            self.ports  = ports 
            self.routes = routes 
            self.ships  = ships
            self.matrix = matrix

        else:

            ports_file = input_file[0]
            routes_file= input_file[1]
            ships_file= input_file[2]

            self.add_ports(ports_file)
            self.add_routes(routes_file)
            self.add_ships(ships_file)
            self.output(self.archivo)

    def calculate_metrics(self):
        
        for ship in self.ships.values():
            total_time = ship.end_time - ship.start_time
            print(f"Barco {ship.ship_id} - "
                            f"Tiempo total itinerario cumplido: {total_time} unidades de tiempo\n")

        total_wait_time_routes = sum(ship.total_wait_time_routes for ship in self.ships.values())
        total_wait_time_ports = sum(ship.total_wait_time_ports for ship in self.ships.values())
        num_events = len(self.ships)
        avg_wait_time_routes = total_wait_time_routes / num_events if num_events > 0 else 0
        avg_wait_time_ports = total_wait_time_ports / num_events if num_events > 0 else 0
        print(f"Tiempo promedio de espera en rutas: "
                    f"{avg_wait_time_routes:.2f} unidades de tiempo\n")
        print(f"Tiempo promedio de espera en puertos: "
                f"{avg_wait_time_ports:.2f} unidades de tiempo\n")
        
    # formar formato pedido
    def output(self, archivo):
        for ship in self.ships.values():
            archivo.write(f"ship;{ship.ship_id};{ship.name};"
                          f"{ship.itinerary[0]};{ship.speed};0.0\n")
        for port in self.ports.values():
            archivo.write(f"port;{port.port_id};{port.name}\n")
        for route in self.routes.values():
            archivo.write(f"route;{route.initial_port_id}-"
                          f"{route.final_port_id};1\n")
