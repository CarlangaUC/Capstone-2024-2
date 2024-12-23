from clases.manager import Manager


manager = Manager()


############### Input automatico ###########

""" Observaciones:
    - No funciona calculate metrics en este caso
"""

n_ports = 2
manager.add(n_ports=n_ports)

t_simulacion = 2000

manager.processes()
manager.step_run(t_simulacion,sleep_time=0)


# RUTAS NO TIENE EL ATRIBUTO DE CAPACITY ??? PORQUEE