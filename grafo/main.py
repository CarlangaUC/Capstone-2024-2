# import env
from clases.clases import Ship, Port, Route
import simpy

env = simpy.Environment()
puerto_1 = Port(env, "san antonio", 100)
puerto_2 = Port(env, "valparaiso", 100)
puerto_3 = Port(env, "antofagasta", 100)
ruta_1 = Route(1, puerto_1, puerto_2, 10)
ruta_2 = Route(2, puerto_2, puerto_3, 15)
ruta_3 = Route(3, puerto_3, puerto_1, 8)
ship_1 = Ship(env, "barco1", 1, puerto_1)
ship_2 = Ship(env, "barco2", 1, puerto_2)
ship_3 = Ship(env, "barco3", 1, puerto_3)
env.process(ship_1.drive(ruta_1))
env.process(ship_2.drive(ruta_2))
env.process(ship_3.drive(ruta_3))
env.run(until=15)
