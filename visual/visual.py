import searoute as sr
import folium
import folium.plugins as plugins
from datetime import datetime,timedelta  


class Visual():
    def __init__(self,map):
        self.map = map
        self.features = []
        self.time = []
        self.routes = {}
        self.ports = {}
        self.ships ={}
        self.simulation_name = "test"
        self.date = datetime(2017, 6, 1)

    # Estas funciones añaden la info a la clase
    
    ## Añadir Puertos 
    def add_port(self,port):
        self.ports[port["id"]]=port


    ## Añadimos rutas
    def add_route(self,route):
        id = route["id"]
        ruta = {}        
        origin,destination = self.get_locations(route)
        path = self.get_shortest_path(origin,destination)
        ruta = {"port_1":route["puerto_1"],"port_2":route["puerto_2"],"path":path}
        self.routes[id]=ruta

    ## Añadir Barcos 
    # Aca en particular en los barcos calculamos la ruta mas
    # corta entre dos puertos y vemos cuales son los lugares
    # en donde estara el barco en la simulacion guardadas en 
    # la variable locations

    def add_ship(self,ship):
        id_route = ship["route"]
        index = []
        self.ships[ship["id"]] = ship
        path = self.routes[id_route]["path"]
        for progress in ship["progress"]:
           index.append(int(progress*len(path)))
        locations = [path[i] for i in index]
        locations= [[lon, lat] for lat, lon in locations]
        
        # Enviamos los lugares donde estara el barco en la simulacion 
        # a la funcion feature
        self.add_feature(locations) 

    # Añadimos un manejo del tiempo, se guardara en una lista 
    def add_time(self,time):
        for t in range(0,time):
            current_date = self.date + timedelta(days=t)
            self.time.append(current_date.strftime("%Y-%m-%dT00:00:00"))            

    # Funcion que obtiene las coordenadas de los puertos de interes de una
    # ruta 
    def get_locations(self,route):
        """Funcion que retorna las coordenadas de los puertos asociadas
        a una ruta de interes"""
        
        p1 = route['puerto_1']
        p2 = route['puerto_2']
        origin = self.ports[p1]["location"]
        destination = self.ports[p2]["location"]
        return origin, destination

    def get_shortest_path(self,origin,destination):
        """ Funcion que retorna una lista de puntos de la ruta mas corta"""
        route = sr.searoute(origin[::-1], destination[::-1])

        # for i in route:
        #     print(route[i])
        #     print("\n")
            

        route_folium= [sublista[::-1] for sublista in route["geometry"]["coordinates"]]


        # folium.PolyLine(route_folium, tooltip="Coast").add_to(self.map)
        plugins.AntPath(reverse="False", locations = route_folium,dash_array=[20,30],color="blue"   
).add_to(self.map)
        self.map.fit_bounds(self.map.get_bounds()) # Centrar el zoom del mapa 
        return route_folium

    def add_markers(self):
        # Añade marcadores a las entidades " estaticas" (las que no se muevan)
        for port in self.ports:
            name =self.ports[port]["name"]
            location =self.ports[port]["location"]
            state=(self.ports[port]["state"])
            if state!="True":
                state = False
            else:
                state =True
    
            color = "green" if state else "red"
            icon = "anchor-circle-check" if state else "anchor-circle-xmark"
            folium.Marker(
            location=location,
            popup=f"Locacion:{location}\nCapacidad: 100 barcos",
            tooltip=f"Puerto de {name}",
            icon=folium.Icon(icon=icon, prefix="fa", color=color)  # Icono de ancla con Font Awesome
        ).add_to(self.map)


    def add_feature(self,info):
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
            "weight": 0,
            
        },
        },
        }]
        # Guardamos las features, basicamente el barco con sus posiciones {info} en el {self.time}
        self.features.append(feature)

    def run(self):
        self.add_markers()
        # Este plugin se encarga de mover el barco!
        # hay que darle las features del proyecto que se
        # inicializan con la funcion add_feature

        feat = self.features[0] +self.features[1]+self.features[2] + self.features[3]
        
        plugins.TimestampedGeoJson(
            {
                "type": "FeatureCollection",
                # "features": self.features[0] +self.features[1]
                "features": feat
            },
            period="P1D",
            auto_play=False,
            loop=False,
            # add_last_point=True,
        ).add_to(self.map)
        
        
        
    def save_map(self):
        self.map.save(f"{self.simulation_name}.html")

def create_simulation(ships,ports,routes,time,simulation_name):
    tile_1 = "OpenStreetMap"
    m = folium.Map(tiles=tile_1,        prefer_canvas=True)

    visual = Visual(m)
    for port in ports:
        visual.add_port(ports[port])
    for route in routes:
        visual.add_route(routes[route])
    for ship in ships:
        visual.add_ship(ships[ship])
    visual.simulation_name = simulation_name
    visual.add_time(time)
    visual.run()
    visual.save_map()

