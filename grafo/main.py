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
manager.add("ports.txt", "routes.txt", "ships.txt")
manager.processes()
manager.run(200)

manager.calculate_metrics()
