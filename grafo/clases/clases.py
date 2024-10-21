UNIT_TIME = 1


class Ship:
    def __init__(self, env, name, speed, port):
        self.env = env
        self.name = name
        self.speed = speed
        self.port = port
        self.pos = 0
        self.route = None

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
    def __init__(self, env, name, capacity):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.ships = []


class Route:
    def __init__(self, route_id, initial_port, final_port, dist):
        self.route_id = route_id
        self.initial_port = initial_port
        self.final_port = final_port
        self.dist = dist
