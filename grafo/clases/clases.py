import simpy
UNIT_TIME = 1


class Ship:
    ship_id = 0

    def __init__(self, env, name, speed, port):
        self.env = env
        self.name = name
        self.speed = speed
        self.port = port
        self.ship_id = Ship.ship_id
        self.pos = 0
        self.route = None
        Ship.ship_id += 1

    def drive(self, route):
        if route.initial_port != self.port:
            yield self.env.timeout(0)
        else:
            self.route = route
            while self.pos < route.dist:
                print(f"{self.name}, ruta {route.route_id}, posicion: {self.pos}, tiempo simulacion {self.env.now}")
                self.pos += self.speed
                yield self.env.timeout(UNIT_TIME)
            route.final_port.ships.append(self)


class Port:

    def __init__(self, env, name, capacity, port_id):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.port_id = port_id
        self.ships = []


class Route:
    route_id = 0

    def __init__(self, env, initial_port, final_port, dist):
        self.env = env
        self.initial_port = initial_port
        self.final_port = final_port
        self.dist = dist
        self.route_id = Route.route_id
        Route.route_id += 1


class Manager:

    def __init__(self):
        self.env = simpy.Environment()
        self.ships = {}
        self.ports = {}
        self.routes = {}

    def ports_generator(self, ports_file):
        with open(ports_file) as file:
            for line in file:
                data = line.strip().split(";")
                yield Port(self.env, data[0],
                           int(data[1]), int(data[2]))

    def routes_generator(self, routes_file):
        with open(routes_file) as file:
            for line in file:
                data = line.strip().split(";")
                yield Route(self.env, self.ports[int(data[0])],
                            self.ports[int(data[1])], int(data[2]))

    def ships_generator(self, ships_file):
        with open(ships_file) as file:
            for line in file:
                data = line.strip().split(";")
                yield Ship(self.env, data[0], float(data[1]),
                           self.ports[int(data[2])])

    def add_ports(self, ports_file):
        for port in self.ports_generator(ports_file):
            self.ports[port.port_id] = port

    def add_routes(self, routes_file):
        for route in self.routes_generator(routes_file):
            self.routes[route.route_id] = route

    def add_ships(self, ships_file):
        for ship in self.ships_generator(ships_file):
            self.ships[ship.ship_id] = ship

    def add(self, ports_file, routes_file, ships_file):
        self.add_ports(ports_file)
        self.add_routes(routes_file)
        self.add_ships(ships_file)

    def processes(self, routes_id):
        for ship, route_id in zip(self.ships.values(), routes_id):
            self.env.process(ship.drive(self.routes[route_id]))

    def run(self, until):
        self.env.run(until=until)