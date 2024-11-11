import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

datos = [

    [[["", "Barco,Coraza,3,Chips"], [""], ["Puerto,Abayarde,1,"]],
     [[""], [""], [""]],
     [[""], ["Barco,Titanic,1,Abayarde"], [""]]],
    
    [[[""], [""], ["Puerto,Abayarde,1,"]],
     [[""], ["Barco,Coraza,3,Chips"], ["Barco,Titanic,1,Abayarde"]],
     [[""], [""], [""]]],
    
    [[[""], [""], ["Puerto,Abayarde,1,Titanic"]],
     [[""], [""], [""]],
     [[""], ["Barco,Coraza,3,Chips"], [""]]]
]

def crear_puertos(ax, estado_inicial):
    puertos = []
    for i in range(len(estado_inicial)):
        for j in range(len(estado_inicial[i])):
            for elemento in estado_inicial[i][j]:
                if "Puerto" in elemento:
                    puerto_info = elemento.split(",")
                    puerto_nombre = puerto_info[1]
                    ax.add_patch(plt.Rectangle((j, 2 - i), 1, 1, fill=True, color="red", alpha=0.5, zorder=1))
                    ax.text(j + 0.5, 2 - i + 0.5, puerto_nombre, color='black', ha='center', va='center', fontsize=10, zorder=2)
                    puertos.append((j + 0.5, 2 - i + 0.5, puerto_nombre))  
    return puertos

def inicializar_barcos(ax, estado_inicial):
    barcos = []
    for i in range(len(estado_inicial)):
        for j in range(len(estado_inicial[i])):
            for elemento in estado_inicial[i][j]:
                if "Barco" in elemento:
                    barco_info = elemento.split(",")
                    barco_name = barco_info[1]
                    barco_position = (j + 0.5, 2 - i + 0.5)
                    barco = ax.scatter(*barco_position, s=400, c='blue', zorder=3)  # Aumentar el tamaño para mejor visibilidad
                    texto_barco = ax.text(*barco_position, barco_name, color='black', ha='center', va='center', fontsize=10, zorder=4)
                    barcos.append((barco, texto_barco, barco_position, barco_info))  
    return barcos

def actualizar_barcos(frame, barcos, datos):
    estado_actual = datos[frame]

    for barco, texto_barco, _, barco_info in barcos:
        barco_nombre = barco_info[1]
        barco_destino = barco_info[3]

        barco_position = (-10, -10)

        for i in range(len(estado_actual)):
            for j in range(len(estado_actual[i])):
                for elemento in estado_actual[i][j]:
                    if elemento == f"Barco,{barco_nombre},{barco_info[2]},{barco_destino}":
                        if any(f"Puerto,{barco_destino}" in el for el in estado_actual[i][j]):
                            barco_position = (-10, -10)  # Simular desaparición al llegar al puerto
                        else:
                            barco_position = (j + 0.5, 2 - i + 0.5)
                        break  
                else:
                    continue
                break
        
        barco.set_offsets(barco_position)
        texto_barco.set_position(barco_position)

def animar(datos):
    fig, ax = plt.subplots()
    
    largo = len(datos[0])
    ax.set_xlim(0, largo)
    ax.set_ylim(0, largo)
    ax.set_xticks(np.arange(0, largo, 1))
    ax.set_yticks(np.arange(0, largo, 1))
    ax.grid(True)
    
    crear_puertos(ax, datos[0])  
    barcos = inicializar_barcos(ax, datos[0])  
    
    ani = animation.FuncAnimation(fig, actualizar_barcos, frames=len(datos), fargs=(barcos, datos), interval=500, blit=False)
    
    ani.save("animacion_barcos.gif", writer='pillow', fps=2)

    
    plt.show()

animar(datos)
