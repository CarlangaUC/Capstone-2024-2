# import env
import simpy
import matplotlib.pyplot as plt
import numpy as np
from clases.clases import Ship, Port

## Codigo simple para ver solamente la estructura y hacerme una idea
# Cosas pendientes:
# 1.- mejorar el sistema de rutas, es muy simple lo que implemente
# 2.- sistema de encallamiento de los barcos, aveces hay barcos en encallan 
#   en el agua esperando un lugar sobretodo los de comercio

# 3.-  ver el tema de colisiones con otros barcos, esto va de la mano con el punto 1.

# 4.- algun tipo de animacion basica, quizas la libreria manim pueda servir


p1 = (0,0) # Posicion puerto 1
p2 = (1,1) # Posicion puerto 2
p3 = (3,1) # Posicion puerto 3
v= p2/np.linalg.norm(p2) # vector director del puerto 1 al 2
v_1= p3/np.linalg.norm(p2) # Vector director del puerot 1 al 3
speed = 0.1


env = simpy.Environment()
ship_1= Ship(env,"Barco A", p1,v,speed,p2)
ship_2= Ship(env,"Barco B", p1,v_1,speed,p3)
env.run(until=15)



