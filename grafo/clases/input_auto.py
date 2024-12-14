from clases.agentes import Ship,Port,Route
import random
import math

## Por simplicidad use distribuciones uniformes, se puede cambiar
# a distribuciones que tengan mas sentido dependiendo del atributo

def generate_agents(env, num_ports, debug = False):
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
    ships,used_routes = gen_ships(env, num_ships, num_ports, all_route)

    # Generamos las rutas
    routes = gen_route(env, used_routes)

    matrix =  gen_matrix(num_ports, routes)


    
    if debug:
        # print(used_routes)
        # print(f"Max capacidad: {global_capacity}\nCantidad de barcos: {num_ships}\nMaxima cantidad de rutas entre puertos: {max_routes}")
        # print(f"{all_route}") 
        # for port in ports:
        #     print(ports[port])
        pass

    return ports, routes, ships, matrix



def gen_ports(env,num_ports):
    """
    Dado un numero de puertos genera puertos aleatorios de la clase Ports

    Input:
    num_ports = Numero de puertos a generar

    Output:
    ports -> Diccionario con clases Port   
    global_capacity -> La suma de todas las capacidades de los puertos
       
    """

    ports = {}
    global_capacity = 0
    for port in range(0,num_ports):
        name = f"Puerto {port}"
        capacity = int(random.uniform(1,50))
        global_capacity+=capacity
        ports[port] = Port(env,name,capacity,port)
    return ports, global_capacity

def all_routes(num_ports):
    """
    Input:

    num_ports -> Numero entero, representa la cantidad de puertos que existen

    Output: 

    all_routes -> Lista de todas las rutas posibles en formato string
                VER EJEMPLO:

    Ejemplo:
    Suponiendo dos puertos con ID 0,1 respectivamente
    all_routes == ["0-1","1-0"]

    
    """
    all_routes = {}
    for i in range(num_ports):
        for j in range(num_ports):
            if i != j:  
                if i in all_routes:
                    all_routes[i].append(f"{i}-{j}")
                else:
                    all_routes[i] = []
                    all_routes[i].append(f"{i}-{j}")
    return all_routes 

def gen_ships(env,num_ships, num_ports,all_routes):
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

    for ship in range(0,num_ships):

        # Generamos un largo del itinerario aleatorio
        num_tasks=  random.randint(1, 20)
        name = f"Barco {ship}"
        speed = gen_velocity() 
        
        # Generamos un puerto del id aleatorio
        port_id = random.randint(0, num_ports-1)
        recharge = gen_recharge()

        # Generamos el itinerario y las rutas que se usaran
        itinerary, used_routes = gen_itinerary(num_tasks, port_id, all_routes, used_routes) 
        
        # Generar boleano aleatorio
        cycles = random.random() < 0.5 

        # Guardar la clase Ship en el diccionario con su id
        ships[ship] = Ship(env,name,speed,port_id,cycles,recharge,itinerary)

    return ships, used_routes

def gen_itinerary(num_tasks, port_id, all_routes, used_routes):

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

    for task in range(0,num_tasks):
        next_route = random.choice(all_routes[port_id])
        used_routes.add(next_route)
        next_port_id = int(next_route.split("-")[1])
        itinerary.append(next_port_id)
        port_id = next_port_id
    
    return itinerary,used_routes

def gen_route(env,used_routes):
    # PUEDE NO CUMPLIRSE LA DESIGULADAD TRINAGULAR
    # REVISAR

    """
    Input:

    used_routes -> Todas las rutas que usaran los barcos

    Output:

    routes      -> Diccionario del estilo {id:<class Port>}

    """

    routes = {}
    used_routes = list(used_routes)

    for route in used_routes:
        initial_port_id= int(route.split("-")[0])
        final_port_id = int(route.split("-")[1])
        dist = gen_dist()
        capacity = gen_capacity_route()
        weather = gen_weather()
        security = gen_security()
        regulations = gen_regulations()
        routes[route] = Route(env, initial_port_id, final_port_id, dist, capacity, weather, security, regulations)

    return routes

def gen_matrix(num_ports, routes):
    """
    Input:

    num_ports -> Numero de puertos    
    routes    -> Diccionario de las clases Route 
    
    Output:
    
    matrix    -> Matriz de adyacencia

    """

    matrix = [[0 for _ in range(num_ports  )] for _ in range(num_ports )]
    for route in routes:
        matrix[routes[route].initial_port_id][routes[route].final_port_id] = route
    return matrix

def gen_velocity():
    return int(random.uniform(1, 5))

def gen_recharge():
    return int(random.uniform(1, 20))

def gen_dist():
    return random.uniform(45, 50)

def gen_capacity_route():
    return random.randint(50, 100)

def gen_weather():
    return random.randint(0,100)

def gen_security():
    return random.randint(0,100)

def gen_regulations():
    return random.randint(0,100)
