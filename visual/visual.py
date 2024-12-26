import searoute as sr
import folium
import folium.plugins as plugins
from datetime import datetime,timedelta  

class Visual():

    def __init__(self, map):
        self.map = map
        self.features = []
        self.time = []
        self.routes = {}
        self.ports = {}
        self.ships ={}
        self.output_path= "test"
        self.date = datetime(2017, 6, 1)
    
    def add_port(self, port):
        # Añadir Puertos dado el diccionario
        self.ports[port["id"]]=port

    def add_route(self, route):
        """
        Esta funciion carga la info de las rutas a la clase
        ademas dada las coordenadas de sus respectivos puertos
        calcula la ruta mas corta con la funcion get_shortest_path

        Input: 
        route -> Diccionario con la informacion de rutas

        Output: None

        """

        id = route["id"]
        ruta = {}        
        origin,destination = self.get_locations(route)
        path = self.get_shortest_path(origin,destination)
        ruta = {"port_1":route["puerto_1"],"port_2":route["puerto_2"],"path":path}
        self.routes[id]=ruta

    def add_ship(self, ship):

        """
        Se añaden la info de los barcos a la simulacion

        Ademas vemos cuales son los lugares en donde estara 
        el barco en la simulacion guardadas en 
        la variable locations 

        Input:

        Output:

        """

        id_route = ship["route"]
        index = []
        self.ships[ship["id"]] = ship
        
        # Obtenemos la ruta donde esta el barco
        path = self.routes[id_route]["path"]

        for progress in ship["progress"]:
           index.append(int(progress*len(path)))

        locations = [path[i] for i in index]
        locations= [[lon, lat] for lat, lon in locations]
        
        # Enviamos los lugares donde estara el barco en la simulacion 
        # a la funcion feature
        self.add_feature(locations) 

    def add_time(self, time):
        """
        Se maneja el tema del tiempo, esta hecho para trabajar en dias
        pero se puede modificar y generalizar

        Al final se agrega a una lista self.time el dia particular al cual
        corresponde el timepo discreto

        Input: 
         
        time -> Numero de tiempos de la simulacion
        
        Output: None

        
        """


        for t in range(0, time):
            current_date = self.date + timedelta(days=t)
            self.time.append(current_date.strftime("%Y-%m-%dT00:00:00"))            

    def get_locations(self, route):
        """
        Input: 
        route -> Diccionario con info de una ruta

        Output:
        origin      -> coordenadas de un puerto
        destination -> coordenadas de un puerto
        
        Funcion que retorna las coordenadas de los puertos asociadas
        a una ruta de interes
        
        """
        
        p1 = route['puerto_1']
        p2 = route['puerto_2']

        origin = self.ports[p1]["location"]
        destination = self.ports[p2]["location"]

        return origin, destination

    def get_shortest_path(self, origin, destination):
        """
        Funcion que retorna una lista de puntos de la ruta mas corta
        
        Input:

        origin      -> Coordenada 
        destination -> Coordenada
        Output:

        route_folium -> Retorna una lista de coordenadas 
        
        """

        # Usando la libreria searoute obtenemos una lista de puntos de la ruta mas corta
        # entre dos coordenadas
        route = sr.searoute(origin[::-1], destination[::-1])

        # dejamos la lista de puntos de la ruta mas corta en un formato tal que 
        # sea compatible con la libreria folium
        route_folium= [sublista[::-1] for sublista in route["geometry"]["coordinates"]]


        # añade al mapa inea que une los puntos de la ruta mas corta SIN MOVIMINETO 
        # folium.PolyLine(route_folium, tooltip="Coast").add_to(self.map)

        # añade al mapa linea que une los puntos de la ruta mas corta CON MOVIMINETO
        plugins.AntPath(reverse="False", locations = route_folium,dash_array=[20,30],color="blue" ).add_to(self.map)
        
        # Centrar el zoom del mapa
        self.map.fit_bounds(self.map.get_bounds())  

        return route_folium

    def add_markers(self):
        """

        Añade marcadores a entidades estaticas en el mapa
        
        Input:  None
        Output: None
        
        """
        # Añade marcadores a las entidades " estaticas " (las que no se muevan)
        # osea a los puertos en este caso

        for port in self.ports:
            name     = self.ports[port]["name"]
            location = self.ports[port]["location"]
            state    = (self.ports[port]["state"])

            if state!="True":
                state = False
            else:
                state =True
    
            color = "green" if state else "red"
            icon = "anchor-circle-check" if state else "anchor-circle-xmark"

            # añade el marcador/icono al mapa

            folium.Marker(
            location=location,
            popup=f"Locacion:{location}\nCapacidad: 100 barcos",
            tooltip=f"Puerto de {name}",
            icon=folium.Icon(icon=icon, prefix="fa", color=color)  # Icono de ancla con Font Awesome
        ).add_to(self.map)


    def add_feature(self, info):
        """

        Funcion que añade un objeto llamado feature (caracteristicas)
        a la lista features, cada feature tiene la informacion de la posicion
        de un barco en el tiempo, con su geometria, color, etc...
        
        El formato de este objeto esta hecho de tal forma que sea reconocido
        por la libreria TimestampedGeoJSON, asi se podra visualizar y manejar
        el movimiento de los barcos durante el tiempo

        Input:  Info

        Output: None
        
        """

        # Necesario este objeto para usar TimestampedGeoJSON

        feature= [{
            "type": "Feature",
            "geometry": {
            "type": "LineString",
            "coordinates": info,
        },
            "properties": {
            "times": self.time,
            "style": {
            "color": "red",
            "weight": 0,},},
        }]

        self.features.append(feature)

    def run(self):
        """

        Se agrega todas las caracteristicas finales al mapa
        tales como marcadores y movimiento

        Input : None
        Output: None

        """

        # Se añaden los marcadores al mapa
        self.add_markers()


        n = len(self.features)

        # TimestampedGeoJSON necesita una suma de listas de las caracteristicas
        features = sum(self.features[:n], []) 

        # Este plugin se encarga de mover el barco!
        # Debemos añadirle ciertos atributos

        plugins.TimestampedGeoJson(
            {
                "type": "FeatureCollection",
                "features": features 
            },
            period="P1D",
            auto_play=False,
            loop=False,
        ).add_to(self.map)
        
        
        
    def save_map(self):
        # Guarda el mapa en un archivo html

        self.map.save(f"{self.output_path}.html")

def create_simulation(ships, ports, routes, time, type, output_path):
    """

    Esta funcion se encarga de inicializar la clase visual 
    ejecutando sus funciones para guardar el archivo 
    que contiene la visualizacion en .html 

    Input:

    ships  -> Diccionario con informacion de los barcos
    ports  -> Diccionario con informacion de los puertos 
    routes -> Diccionario con informacion de los rutas 
    time   -> Tiempo de la simulacion
    output_path-> Nombre de la ruta donde se guardara el archivo
                    .html junto con su nombre  

    Output:

    -> Sin output 

    """

    # Creamos el objeto mapa de la clase Map de folium
    mapa = folium.Map(tiles=type, prefer_canvas=True)

    # Inicializamos la clase Visual
    visual = Visual(mapa)

    # Añadimos la informacion de los agentes a la clase Visual
    for port in ports:
        visual.add_port(ports[port])
    for route in routes:
        visual.add_route(routes[route])
    for ship in ships:
        visual.add_ship(ships[ship])
    
    # output path de la simulacion
    visual.output_path = output_path 

    # Tiempos a simular 
    visual.add_time(time)
    visual.run()

    # Guardamos el mapa
    visual.save_map()

