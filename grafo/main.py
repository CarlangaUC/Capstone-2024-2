from clases.manager import Manager


manager = Manager()


############### Input automatico ###########

""" Observaciones:
    - No funciona calculate metrics en este caso
"""

n_ports = 5
manager.add(n_ports=n_ports)

manager.processes()
manager.step_run(20,sleep_time=0)


