from clases.manager import Manager


def manejar_archivo(archivo):
    with open(archivo, "r") as datos_entrada:
        eventos = datos_entrada.strip().split("\n")
    eventos_por_tiempo = {}

    for evento in eventos:
        partes = evento.split(";")
        tiempo = int(partes[-1])
        if tiempo not in eventos_por_tiempo:
            eventos_por_tiempo[tiempo] = []
        eventos_por_tiempo[tiempo].append(evento)

    output = []
    for tiempo in sorted(eventos_por_tiempo.keys()):
        output.append(f"t={tiempo}")
        for evento in eventos_por_tiempo[tiempo]:
            partes = evento.split(";")
            nuevo_evento = (f"event;{partes[1]};{partes[2]};"
                            f"{partes[3]};{partes[4]}")
            output.append(nuevo_evento)

    with open("output.txt", "w") as salida:
        for linea in output:
            salida.write(linea + "\n")


manager = Manager()


############### Input automatico ###########

""" Observaciones:
    - Pendiente arreglar tema de distancias de rutas respeten
      la desigualdad triangular
    - No funciona calculate metrics en este caso
    - Aveces no encuentra ninguna ruta 
    - suele fallar con timepos mas de 10, pendiente arreglar
"""

n_ports = 5
manager.add(n_ports=n_ports)

manager.processes()
manager.run(100)

# manager.calculate_metrics()

################ Input con formato texto #############
# input_file= ["ports.txt", "routes.txt", "ships.txt"]

# manager.add(input_file = input_file)

# manager.processes()
# manager.run(100)

# manager.calculate_metrics()
