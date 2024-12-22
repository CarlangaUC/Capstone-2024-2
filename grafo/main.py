from clases.manager import Manager


manager = Manager()


############### Input automatico ###########

""" Observaciones:
    - No funciona calculate metrics en este caso
"""

n_ports = 2
manager.add(n_ports=n_ports)


manager.processes()
manager.step_run(2000,sleep_time=0)


# RUTAS NO TIENE EL ATRIBUTO DE CAPACITY ??? PORQUEE