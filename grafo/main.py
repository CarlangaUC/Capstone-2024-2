from clases.manager import Manager


manager = Manager()


############### Input automatico ###########

""" Observaciones:
    - Pendiente arreglar tema de distancias de rutas respeten
      la desigualdad triangular
    - No funciona calculate metrics en este caso
"""

n_ports = 5
manager.add(n_ports=n_ports)

manager.processes()
# manager.step_run(2000,sleep_time=0)




# manager.calculate_metrics()

################ Input con formato texto #############
# input_file= ["ports.txt", "routes.txt", "ships.txt"]

# manager.add(input_file = input_file)

# manager.processes()
# manager.run(100)

# manager.calculate_metrics()
