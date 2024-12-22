from visual import create_simulation 
from input_visual import load_simulation

path = "inputs/input_test.txt"
ships,ports,routes = load_simulation(path)
create_simulation(ships,ports,routes,18,"outputs/simulacion")