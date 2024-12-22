from visual import create_simulation 
from input_visual import load_simulation

time     = 18
# Tipo de mapa, pueden probar con distintos tipos ejemplos:
# type = "Cartodb dark_matter", type= "OpenStreetMap" 

# Mas info en https://python-visualization.github.io/folium/latest/user_guide/raster_layers/tiles.html
type     = "CartoDB positron" 

path     = "inputs/input_presentacion.txt"
out_path = "outputs/simulacion"

ships, ports, routes = load_simulation(path)
create_simulation(ships, ports, routes, time, type, out_path)