def load_simulation(path, debug=False):
    """

    Funcion que se encarga de leer el input.txt y retornar la informacion
    de los agentes de la simulacion para la visualizacion

    Importante notar que no esta asociado a la simulacion de grafos
    tiene su propio formato

    Input: 

    path -> string de la ruta del input.txt


    Output:

    ships  -> Diccionario con info de los barcos
    ports  -> Diccionario con info de los puertos 
    routes -> Diccionario con info de los rutas 
    
    """

    ports = {}
    ships = {}
    routes = {}

    with open(path, 'r') as file:
        for line in file:
            line = line.strip()  
            if line.startswith("routes"):
                _,p1,p2,id = line.split(';')
                routes[id] = {        "puerto_1":p1,
                                      "puerto_2":p2,
                                        "id":id}
            if line.startswith("port"):
                _, name, location, state,id= line.split(';')
                if id in ports:
                    pass
                else:

                    ports[id] = {"name":name,
                                "location":list(map(float, location.strip("[]").split(','))),
                                "state":state,
                                "id":id}
            if line.startswith("ship"):
                _, name, progress, start,objective,id,route= line.split(';')
                if id in ships:
                    ships[id]["state"].append(bool(state))
                    ships[id]["progress"].append(float(progress))
                else:
                    ships[id] = {"name":name,
                                "progress":[float(progress)],
                                "state":[bool(state)],
                                "start":start,
                                "objective":objective,
                                "route":route,
                                "id":id}

    if debug:
        print(f"En esta simulacion se cargaron lo siguiente:\nBarcos: {ships}\nPuertos: {ports}\nRutas:{routes}")
        print(f"Los id:\nBarcos: {list(ships.keys())}\nPuertos: {list(ports.keys())}\nRutas:{list(routes.keys())}")
    return ships,ports,routes