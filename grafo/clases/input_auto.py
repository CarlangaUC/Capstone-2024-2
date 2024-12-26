from clases.agentes import Ship, Port, Route
import numpy as np
import random
import math
from geopy.distance import geodesic 
 
def generate_agents(env, num_ports, debug=False):
    """
    Input:
    env       -> Entorno de simpy
    num_ports -> Numero de puertos a generar

    Output:
    ports      -> Diccionario de {id:<clase Port>}
    routes     -> Diccionario de {id:<clase Route>}
    ships      -> Diccionario de {id:<clase Ship>}
    """

    # Generaremos las clases solo de las rutas que vamos a utilizar
    # Generamos los puertos
    ports, global_capacity = gen_ports(env, num_ports)

    # Generamos un entero aleatorio que representa la cantidad
    # de barcos que tendra nuestra simulacion
    num_ships = random.randint(1, global_capacity)

    # Calculamos el maximo de rutas posibles entre puertos
    max_routes = math.comb(num_ports, 2)*2

    # Obtenemos todas las rutas posibles entre puertos
    all_route = all_routes(num_ports)

    # Generamos los barcos junto con las rutas que se usaran a priori
    ships, used_routes = gen_ships(env, num_ships, num_ports, all_route)

    # Generamos las rutas
    routes = gen_route(env, used_routes)

    matrix = gen_matrix(num_ports, routes)

    if debug:
        if num_ports <4:
            with open('debug.txt', 'w') as debugg:
                debugg.write(f"BARCOS GENERADOS:{num_ships}\nRUTAS GENERADOS: {len(all_route)}\n")

                debugg.write("BARCOS\n")
                for id in ships:
                    ship =ships[id]
                    debugg.write(f"Nombre: {ship.name}, Velocidad: {ship.speed}, ID del Puerto: {ship.port_id}, "
          f"Ciclos: {ship.cycles}, Recarga: {ship.recharge}, Itinerario: {ship.itinerary}\n")

                debugg.write("RUTAS\n")
                for id in routes:
                    route = routes[id]
                    debugg.write(f"Puerto Inicial: {route.initial_port_id}, Puerto Final: {route.final_port_id}, "
          f"Distancia: {route.dist}, "
          f"Clima: {route.weather}, Seguridad: {route.security}, "
          f"Regulaciones: {route.regulations}\n")

                debugg.write("Puertos\n")
                for id in ports:
                    port = ports[id]
                    debugg.write(f"Puerto: {port.name}; Capacidad: {port.capacity}, port:{port.port_id}\n") 

    return ports, routes, ships, matrix

def gen_ports(env, num_ports):
    """
    Dado un número de puertos genera puertos aleatorios de la clase Ports

    Input:
    num_ports = Número de puertos a generar

    Output:
    ports -> Diccionario con clases Port
    global_capacity -> La suma de todas las capacidades de los puertos
    """

    ports = {}
    global_capacity = 0
    for port in range(0, num_ports):
        name = f"Puerto {port}"
        capacity = int(random.uniform(1, 50))
        global_capacity += capacity
        ports[port] = Port(env, name, capacity, port)
    return ports, global_capacity

def all_routes(num_ports):
    """
    Input:
    num_ports -> Número entero, representa la cantidad de puertos que existen

    Output:
    all_routes -> Lista de todas las rutas posibles en formato tupla

    Ejemplo:
    Suponiendo dos puertos con ID 0, 1 respectivamente
    all_routes == [(0,1),(1,0)]
    """

    all_routes = {}
    for i in range(num_ports):
        for j in range(num_ports):
            if i != j:
                route = (i, j)
                if i in all_routes:
                    all_routes[i].append(route)
                else:
                    all_routes[i] = []
                    all_routes[i].append(route)
    return all_routes

def gen_ships(env, num_ships, num_ports, all_routes):
    """
    Input:
    num_ships    -> Numero de barcos a generar
    num_ports    -> Numero de puertos en la simulacion
    all_routes   -> Todas las rutas posibles

    Output:
    ships        -> Diccionario de barcos de la clase Ship
    used_routes  -> Las rutas que se usaron por estos barcos
    """

    used_routes = set()
    ships = {}

    for ship in range(0, num_ships):

        # Generamos un largo del itinerario aleatorio
        num_tasks = random.randint(2, 20)
        name = f"Barco {ship}"
        speed = gen_velocity()
        # Generamos un puerto del id aleatorio
        port_id = random.randint(0, num_ports-1)
        recharge = gen_recharge()
        # Probabilidad 0.5 de itinerario cíclico
        cycles = random.random() < 0.5
        # Generamos el itinerario y las rutas que se usaran
        itinerary, used_routes = gen_itinerary(num_tasks, port_id,
                                               all_routes, used_routes,cycles)
        # Guardar la clase Ship en el diccionario con su id
        ships[ship] = Ship(env, name, speed, port_id,
                           cycles, recharge, itinerary)

    return ships, used_routes

def gen_itinerary(num_tasks, port_id, all_routes, used_routes,cycles):
    """
    Input:
    num_tasks   -> Largo del itinerario
    port_id     -> Id del puerto inciial
    all_routes  -> Todas las rutas posibles

    Output:
    itinerary   -> Lista con los id de los puertos que debe visitar
    used_routes -> Conjunto que contiene las rutas que realmente se usaron
    """

    itinerary = []

    for task in range(0, num_tasks):
        next_route = random.choice(all_routes[port_id])
        used_routes.add(next_route)
        next_port_id = next_route[1]
        itinerary.append(next_port_id)
        port_id = next_port_id

    # Si un barco ciclico va al puerto x en su ultimo viaje
    # no queremos que en el siguiente tiempo vaya denuevo al puerto x,
    # sino a uno distinto!, se agrega un puerto mas a su itinerario 
    # por simplicidad
    if itinerary[0] == itinerary[-1] and cycles==True:
        next_route = random.choice(all_routes[port_id])
        used_routes.add(next_route)
        next_port_id = next_route[1]
        itinerary.append(next_port_id)
        port_id = next_port_id



    return itinerary, used_routes

def gen_route(env, used_routes):
    """
    Input:
    used_routes -> Todas las rutas que usaran los barcos

    Output:
    routes      -> Diccionario del estilo {id:<class Port>}
    """
    routes = {}
    used_routes = list(used_routes)
    done = set()
    sample_points = {}
    for route in used_routes:
        initial_port_id = route[0]
        final_port_id = route[1]
        other_route = f"{final_port_id}-{initial_port_id}"
        route_name = f"{initial_port_id}-{final_port_id}"

        # Cumpla la simetria
        if other_route in done:
            dist = routes[other_route].dist
        else:
            done.add(route_name)
            dist,sample_points = gen_dist(initial_port_id,final_port_id,sample_points)
        capacity = gen_capacity_route()
        weather = gen_weather()
        security = gen_security()
        regulations = gen_regulations()
        routes[route_name] = Route(env, initial_port_id, final_port_id, dist,
                                   capacity, weather, security, regulations)
        
    for route in routes:
        print(f"{route}: {routes[route].dist}")
    return routes

def gen_random_point():
    latitude = random.uniform(-90, 90)
    longitude = random.uniform(-180, 180)
    return latitude, longitude

def gen_dist(id_in,id_out,sample_points):
    while id_in not in sample_points:
        lat, lon = gen_random_point()
        p1 = (lat, lon)
        if p1 not in list(sample_points.values()):
            sample_points[id_in] = p1

    while id_out not in sample_points:
        lat, lon = gen_random_point()
        p2 = (lat, lon)
        if p2 not in list(sample_points.values()):
            sample_points[id_out] = p2
    
    p1 = sample_points[id_in]
    p2 = sample_points[id_out]

    return geodesic(p1,p2).km, sample_points
    
def gen_matrix(num_ports, routes):
    """
    Input:
    num_ports -> Número de puertos
    routes    -> Diccionario de las clases Route

    Output:
    matrix    -> Matriz de adyacencia
    """

    matrix = [[0 for _ in range(num_ports)] for _ in range(num_ports)]
    for route in routes:
        matrix[routes[route].initial_port_id][routes[route].final_port_id] = route
    return matrix

def gen_velocity():
    return int(random.uniform(30, 100))

def gen_recharge():
    return int(random.uniform(1, 20))

def gen_capacity_route():
    return random.randint(50, 100)

def gen_weather():
    return random.randint(0, 100)

def gen_security():
    return random.randint(0, 100)

def gen_regulations():
    return random.randint(0, 100)