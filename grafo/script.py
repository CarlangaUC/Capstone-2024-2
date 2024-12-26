# Paso 1: Convertir los datos a una estructura de listas
eventos = datos_entrada.strip().split("\n")
eventos_por_tiempo = {}

# Agrupar eventos por tiempo (el último campo en cada evento)
for evento in eventos:
    partes = evento.split(";")
    tiempo = int(partes[-1])
    if tiempo not in eventos_por_tiempo:
        eventos_por_tiempo[tiempo] = []
    eventos_por_tiempo[tiempo].append(evento)

# Paso 2: Crear el nuevo formato
output = []
for tiempo in sorted(eventos_por_tiempo.keys()):
    output.append(f"t={tiempo}")
    for evento in eventos_por_tiempo[tiempo]:
        partes = evento.split(";")
        # Modificar el evento para ajustarse al formato requerido
        nuevo_evento = f"event;{partes[1]};{partes[2]};{partes[3]};{partes[4]}"
        output.append(nuevo_evento)