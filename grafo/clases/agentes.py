import clases.func_params as f_p
import simpy


class Ship:
    ship_id = 0

    def __init__(self, env, name, speed, port_id,
                 cycles, recharge, itinerary):
        self.env = env
        self.name = name
        self.speed_ = speed
        self.port_id = port_id
        self.ship_id = Ship.ship_id
        self.load = 0
        self.pos = 0
        # True si su itinerario es cíclico, sino False
        self.cycles = bool(cycles)
        self.route_id = ""
        Ship.ship_id += 1
        self.recharge_ = recharge
        self.itinerary = itinerary
        self.actual_port = port_id

        # Métricas
        # Tiempo total del itinerario
        self.start_time = 0
        self.end_time = 0
        # Tiempo de espera en rutas y puertos
        self.total_wait_time_routes = 0
        self.total_wait_time_ports = 0

    @property
    def recharge(self):
        return f_p.recharge_dist(self.recharge_)

    @property
    def speed(self):
        return f_p.speed_dist(self.speed_)

    def unload(self, filename):
        # simula la descarga del barco, espera según la carga que tiene
        with open(filename, "a") as file:
            file.write(f"event;ES2;{self.ship_id};{self.actual_port};"
                       f"{self.env.now}\n")
        print(f"Barco {self.ship_id} descargando...")
        yield self.env.timeout(self.recharge)

    def drive(self, final_port, route, filename, matriz_adyacencia):
        with route.resource.request() as request:
            print(f"{self.name} esperando...")
            wait_start = self.env.now
            yield request
            self.total_wait_time_routes += self.env.now - wait_start
            while self.pos < route.dist:
                self.pos += self.speed
                pos_total = round(self.pos/route.dist, 2)
                with open(filename, "a") as file:
                    file.write(f"event;ES1;{self.ship_id};{self.actual_port}-"
                               f"{final_port.port_id};{pos_total};"
                               f"{self.env.now}\n")
                print(f"{self.name}, ruta {route.route_id}, "
                      f"posicion: {self.pos}, "
                      f"tiempo simulacion {self.env.now}")
                yield self.env.timeout(f_p.UNIT_TIME)
        with final_port.resource.request() as request:
            wait_start = self.env.now
            yield request
            self.total_wait_time_ports += self.env.now - wait_start
            self.pos = 0
            final_port.ships.append(self.ship_id)
            yield self.env.process(self.unload(filename))
            final_port.ships.remove(self.ship_id)


class Port:

    def __init__(self, env, name, capacity, port_id):
        self.env = env
        self.name = name
        self.capacity = capacity
        self.port_id = port_id
        self.ships = []
        self.open = True
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
        self.route_id = f"{initial_port_id}-{final_port_id}"
        self.ships = []
        self.resource = simpy.Resource(env, capacity=capacity)
        self.open = True
