# import env
from clases.clases import Ship, Port, Route
import simpy

env = simpy.Environment()
puerto_1 = Port(env, "san antonio", 100)
puerto_2 = Port(env, "valparaiso", 100)
ruta_1 = Route(1, puerto_1, puerto_2, 10)
ship_1 = Ship(env, "barco1", 1, puerto_1)
env.process(ship_1.drive(ruta_1))
env.run(until=15)
