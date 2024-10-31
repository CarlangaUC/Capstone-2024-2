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
        self.pos = 0
        self.route_id = -1
        Ship.ship_id += 1


class Port:

    def __init__(self, env, name, capacity, port_id):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.port_id = port_id
        self.ships = []
        # IDEA: el puerto podría tener un resource que sea algo
        # como "operadores" o "gruas" para modelar la capacidad


class Route:
    route_id = 0

    def __init__(self, env, initial_port_id, final_port_id, dist):
        self.env = env
        self.initial_port_id = initial_port_id
        self.final_port_id = final_port_id
        self.dist = dist
        self.route_id = Route.route_id
        Route.route_id += 1


class Manager:

    def __init__(self):
        self.env = simpy.Environment()
        self.ships = {}
        self.ports = {}
        self.routes = {}

    def drive(self, ship_id, route_id):
        route = self.routes[route_id]
        ship = self.ships[ship_id]
        final_port = self.ports[route.final_port_id]
        if route.initial_port_id != ship.port_id:
            yield self.env.timeout(0)
        else:
            ship.route_id = route_id
            while ship.pos < route.dist:
                print(f"{ship.name}, ruta {ship.route_id}, posicion: {ship.pos}, "
                      f"tiempo simulacion {ship.env.now}")
                ship.pos += ship.speed
                yield ship.env.timeout(UNIT_TIME)
            final_port.ships.append(ship_id)

    # estas funciones generator son solo una forma "elegante" de cargar los
    # archivos .txt como instancias
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
                yield Route(self.env, int(data[0]),
                            int(data[1]), int(data[2]))

    def ships_generator(self, ships_file):
        with open(ships_file) as file:
            for line in file:
                data = line.strip().split(";")
                yield Ship(self.env, data[0], float(data[1]),
                           int(data[2]))

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
        for ship_id, route_id in zip(self.ships, routes_id):
            self.env.process(self.drive(ship_id, route_id))

    def run(self, until):
        self.env.run(until=until)
