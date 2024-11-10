import numpy as np
import simpy
UNIT_TIME = 1


class Ship:
    ship_id = 0

    def __init__(self, env, name, speed, port_id):
        self.env = env
        self.name = name
        self.speed = speed
        self.port_id = port_id
        self.ship_id = Ship.ship_id
        self.load = 0
        self.pos = 0
        self.route_id = -1
        Ship.ship_id += 1

    def unload(self, load):
        print(f"Barco {self.ship_id} descargando...")
        yield self.env.timeout(load)

    def drive(self, final_port, load, dist, route_id):
        while self.pos < dist:
            print(f"{self.name}, ruta {route_id}, posicion: {self.pos}, "
                  f"tiempo simulacion {self.env.now}")
            self.pos += self.speed
            yield self.env.timeout(UNIT_TIME)
        with final_port.resource.request() as request:
            yield request
            self.pos = 0
            final_port.ships.append(self.ship_id)
            yield self.env.process(self.unload(load))
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
        self.route_id = f"{initial_port_id}-{final_port_id}"
        self.ships = []


class Manager:

    def __init__(self):
        self.env = simpy.Environment()
        self.ships = {}
        self.ports = {}
        self.routes = {}

    # estas funciones generator son solo una forma "elegante" de cargar los
    # archivos .txt como instancias
    def general_event_loop(self, events_dict):
        for key in events_dict:
            self.event_loop(key, events_dict[key])

    def ship_event_loop(self, ship, events):
        actual_port_id = ship.port_id
        for (final_port_id, load) in events:
            final_port = self.ports[final_port_id]
            route = self.routes[f"{actual_port_id}-{final_port_id}"]
            route.ships.append(ship.ship_id)
            yield self.env.process(ship.drive(final_port, load, route.dist, route.route_id))
            route.ships.remove(ship.ship_id)
            actual_port_id = final_port_id

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
                yield Ship(self.env, data[0], float(data[1]),
                           int(data[2]))

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

    def processes(self, events_tuples):
        for ship_id, events in events_tuples:
            self.env.process(self.ship_event_loop(self.ships[ship_id], events))

    def run(self, until):
        self.env.run(until=until)
