- Titulo: Integrantes, descripcion, proyecto. | Carlos
- Contexto: Uso de simpy, Simulacion discreta de agentes. | Dani
- agentes.py : Explicar agentes, metodos importantes y contexto de atributos | Cleme
- func_param.py : *** | Carlos
- input_auto.py : Explicar como se forman estos inputs, funciones mas importantes. | Basti
- manager.py : Explicar en conjunto con E/R, funcionamiento como tal, y metodos importantes. | Cleme
- main.py : instrucciones, parametros. | Carlos
- visual.py : explicar visualizacion actual, instrucciones. | Basti

# Simulación Marítima 

**Integrantes del equipo**:

- **Clemente Campos**
- **Carlos Olguín**
- **Felipe Cox**
- **Daniel Hidalgo**
- **Bastián Cortés**


**Descripción**: El siguiente repositorio contiene las instrucciones y documentación de la solución planteada por el equipo en torno a la problemática de un simulador marítimo. Para esto se incluye todo lo necesario para entender cómo se corre el código y su funcionamiento.

## Contexto

Este proyecto emplea como base para la modelación del comercio marítimo internacional los paradigmas de simulación basada en agentes y de simulación de eventos discretos. Se diseñaron tres clases para representar los barcos, puertos y rutas, que son los agentes clave en el modelo. Para la SED se utilizó la librería SimPy. Gracias a esto la simulación permite representar cada barco, puerto y ruta como agentes con comportamientos y características definidas, que interactúan en un entorno dinámico modelado en intervalos de tiempo discretos. La simulación incluye eventos clave como el movimiento de los barcos entre los distintos puertos, además del cierre y apertura temporal de puertos y de rutas, con las respectivas consecuencias que generan en el sistema.

### Clases
El archivo [agentes.py](clases/agentes.py) contiene las clases de los tres agentes principales de la simulación, listadas a continuación:
- Ship: clase encargada de representar a un barco. Los siguientes atributos y métodos son los más importantes.
    - env: referencia al Enviroment de SimPy.
    - speed_: float que representa la velocidad base del barco.
    - port_id: id del puerto actual donde se encuentra el barco.
    - ship_id: id único para cada barco.
    - load: int representando la carga del barco.
    - pos: float que representa la posición del barco en la ruta actual.
    - cycles: valor booleano que determina si el itinerario del barco es cíclico o no.
    - route_id: id de la ruta en la cual se encuentra el barco.
    - recharge_: tiempo base que demora el barco en descargar.
    - itinerary: itinerario del barco.
    - recharge(): property que retorna el tiempo de descarga del barco según la distribución usada.
    - speed(): property que retorna el valor de la velocidad.
    - drive(): función que se encarga de mover el barco de un puerto a otro.

- Port: clase encargada de representar un puerto. Los siguientes atributos son los mas importantes.
    - env: referencia al Enviroment de SimPy.
    - capacity: capacidad del puerto.
    - port_id: id único para cada puerto.
    - ships: lista de barcos en el puerto.
    - open: booleano que indica si el puerto está abierto o no.
    - resource: recurso de SimPy que controla el acceso al puerto.

- Route: clase encargada de representar una ruta. Los siguientes atributos son los más importantes.
    - env: referencia al Enviroment de SimPy.
    - initial_port_id: id del puerto inicial de la ruta.
    - final_port_id: id del puerto final de la ruta.
    - dist: largo de la ruta.
    - route_id: id único para cada ruta.
    - ships: lista de barcos en la ruta.
    - resource: recurso de SimPy que controla el acceso a la ruta.
    - open: booleano que indica si la ruta está abierta o no.

### Manager
El archivo [manager.py](clases/manager.py) contiene la clase Manager, que se encarga de generar una simulación particular. Los siguientes atributos y métodos son los más importantes.
- env: referencia al Enviroment de SimPy.
- ships: diccionario donde las llaves son los id's de los barcos y los valores sus instancias asociadas.
- ports: diccionario donde las llaves son los id's de los puertos y los valores sus instancias asociadas.
- routes: diccionario donde las llaves son los id's de las rutas y los valores sus instancias asociadas.
- search_route(): método que se encarga de encontrar una ruta entre dos puertos.
- ship_event_loop(): método que se encarga de llevar a cabo el itinerario de un barco en particular.
- processes(): método que añade el ship_event_loop de cada barco como un proceso.
- run(): método que corre la simulación por un tiempo determinado.
- step_run(): método que corre la simulación esperando un tiempo determinado entre cada intervalo.

El siguiente diagrama de clases indica la relación entre todas las clases:
![image](diagrama.png)

### Input Automático ⚙️

En el archivo [input_auto.py](clases/input_auto.py) se generan aleatoriamente los agentes de la simulación a partir de un número de puertos como input. Se usaron distribuciones uniformes por simplicidad, siempre pensando en que esto puede ser modificado dependiendo del propósito de la empresa. El funcionamiento es el siguiente:

- generate_agents: Función que se encarga de generar todos los agentes llamando a otras funciones y finalmente retorna diccionarios con instancias de las clases (clases definidas en [agentes.py](clases/agentes.py)) más una matriz de adyacencia de las distancias entre rutas .
    - El número de barcos generados se escoge aleatoriamente entre 1 y la capacidad máxima global que pueden almacenar los puertos.
    - También posee un argumento debug el cual por defecto es False. Si se le entrega True se generará un archivo debug.txt el cual retorna la información de todas las entidades generadas.

- gen_ports: Dado un número de puertos genera un diccionario con los puertos aleatorios de la clase [Port](clases/agentes.py#L78), además retorna la suma de todas las capacidades de los puertos.
    - La capacidad máxima de un puerto individual es un numero aleatorio entre 1 y 50.

- all_routes: Recibe el número de puertos que se quieren generar, retorna una lista con todas las tuplas que representen rutas posibles en la simulación.
    - Podrían existir más rutas de las que se generan, eso es algo que se puede generalizar a partir del código.

- gen_ships: Dado un número de barcos (escogido en generate_agents), un número de puertos y una lista con todas las rutas posibles entre puertos se genera un diccionario con los barcos aleatorios de la clase [Ship](clases/agentes.py#L5). Se asume un id secuencial (0,1,...,num_ships-1), la carga y la velocidad se generan con ciertas funciones basadas en distribuciones uniformes (ver el punto Otros). Además se genera el itinerario con la función gen_itinerary y retorna el diccionario con los barcos y las rutas usadas por los barcos.
    - Acá se asume que solo van a existir las rutas que se escogieron al azar
    es claro que también uno poddria considerar más rutas, se puede genralizar.

- gen_itinerary: Recibe un número aleatorio de las tareas que debe realizar el barco (generado en gen_ships), id del puerto inicial, si es cíclico el barco y un set de las rutas que ya se han utilizado, a partir del id inciial se genera aleatoriamente el id del siguiente puerto destino y se agrega al itinerario hasta llenar el itinerario.

- gen_route: Recibe las rutas que se usaron, itera por estas rutas y genera su información. La distancia se genera escogiendo puntos aleatorios en la tierra (latitudes, longitudes aleatorias)y calculando su distancia con la función gen_dist.

- gen_random_point: Genera una latitud y longitud aleatoria.

- gen_dist: Recibe el id inicial y final de una ruta, más los puntos ya generados a los distintos
puertos, se verifica no volver a generar un punto aleatorio a un puerto que ya se le habia generado uno. Retorna la distancia geodésica utilizando la libreria geopy.
    - Hay muchas otras formas de calcular la distancia, se puede generalizar dependiendo del propósito.

- gen_matrix: Dado el número de puertos y clases de rutas se genera la matriz de adyacencia de la simulación la cual tendra las distancias de las rutas.

- Otros: También hay otras funciones como [gen_velocity](/grafo/clases/input_auto.py#L257) cuyo propósito es agregar mayor dinámica o funcionamiento al código. Estas se ubican al final del código del archivo.

### Visualización 🗺️

![](/visual/simulation.gif)

En la carpeta [visual](/visual) se encuentran todas los archivos correspondientes al apartado visual de la simulación.

**Consideraciones**: La visualización está basada en el output que retorna la simulación. Esto se puede generalizar, ya que la idea es dar un primer paso para que adaptando el output de la simulación final se pueda llegar a una visualización similar y adaptable a distintos escenarios. Es por esto que la visualización no está completamente integrada a la simulación.

Funcionamiento de la visualización: Se compone principalmente de 3 archivos

- [input_visual.py](/visual/input_visual.py): En este archivo se encuentra la función [load_simulation](/visual/input_visual.py#L1) que carga un archivo.txt, el archivo.txt que maneja tiene el siguiente formato
    - Se ha implementado el movimiento de los barcos, la función load_simulation es independiente
    de t, las líneas que contienen t son para mejor entendimiento del input.

```
t=0
port;nombre;[lat, lon];estado;ID_Puerto
ship;nombre;posición inicial;puerto inicial;puerto final;ID_Barco;ID_ruta
routes;ID_puerto_1;ID_puerto_2;ID_ruta
t>0
ship;nombre;posicion en tiempo t;puerto inicial;puerto final;ID_Barco;ID_ruta
```

- [visual.py](/visual/visual.py): Este archivo contiene una función importante y una clase
    
    - [Visual](/visual/visual.py#L6): Clase la cual se encarga de manejar todo el aspecto visual 
    con las librerias [folium](https://python-visualization.github.io/folium/latest/) y [searoute](https://pypi.org/project/searoute/), los metodos principales de esta clase son:
         
        - [get_shortest_path](/visual/visual.py#L118): En esta función se utiliza la librería de searoute, en particular la función searoute la cual recibe las coordenadas de dos puntos de la tierra y retorna una objeto especial con la informacion de la ruta mas corta marítima del cual extraemos una lista de las coordenadas de esta ruta, además añadimos al mapa (está en el atributo self.map, objeto de folium) una interpolación de esta ruta.
        
        - [add_feature](/visual/visual.py#L186): recibe la información de un objeto que tenga movimiento y lo agrega a la lista self.features, se podrian agregar mas entidades con movimiento usando esta función, para este proyecto solamente maneja el movimiento de los barcos.
        
        - [run](/visual/visual.py#L220): En esta función se añaden los marcadores (los íconos de los puertos en este proyecto) con la función self.add_markers, además se utiliza el plugin de folium TimestampedGeoJson el cual es el encargado de manejar el movimiento de los barcos en la visualización.

    - [create_simulation](/visual/visual.py#L260): Recibe diccionarios con la información de los el tiempo de la simulación (cuántos intervalos se van a realizar), tipo de mapa, y  una ruta de donde se guardará el archivo .html. En esta función se crea la instancia Map de folium, la cual es la que posee el mapa que se verá en la visualización, inicializamos la clase Visual, añadimos la información de los agentes a la clase y luego ejecutamos métodos de la clase para hacer que todo funcione y retornar la output .html.


- [run.py](/visual/run.py): En este archivo se ejecuta la visualización, se crean los parámetros,se obtienen los agentes y se ejecuta la visualización con la función create_simulation.


### Ejecución 📋


Para ejecutar la simulación se debe ejecutar el archivo [main.py](main.py), en el cual se deberá tener en consideración lo siguiente:

- **Hiperparámetros** : Estos deberan ser escogidos de acuerdo a lo necesitado, lo ínico manual a cambiar es el **n_ports** (número de puertos), los cuales influirían en la cantidad de barcos generados como fue explicado en **Input Automático** y el **t_simulacion** (tiempo de simulación), que indicará la cantidad de tiempo hasta cual la simulación se ejecutará al ser una simulacion discreta.

- **Tiempo** : La simulación correrá hasta cierto tiempo dependiendo de lo especificado, pero además, para simular el tiempo más adecuado entre eventos, se plantea el parámetro **sleep_time** de simpy el cual permite retrasar el tiempo entre cada intervalo como tal, de esta manera permitiendo leer el output de manera mas ordenado, se recomienda con sleep_time del orden de 10^-3 para mejor lectura.
 











### Pre-requisitos 📋

_Que cosas necesitas para instalar el software y como instalarlas_

```
Da un ejemplo
```

### Instalación 🔧

_Una serie de ejemplos paso a paso que te dice lo que debes ejecutar para tener un entorno de desarrollo ejecutandose_

_Dí cómo será ese paso_

```
Da un ejemplo
```

_Y repite_

```
hasta finalizar
```

_Finaliza con un ejemplo de cómo obtener datos del sistema o como usarlos para una pequeña demo_

## Ejecutando las pruebas ⚙️

_Explica como ejecutar las pruebas automatizadas para este sistema_

### Analice las pruebas end-to-end 🔩

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

### Y las pruebas de estilo de codificación ⌨️

_Explica que verifican estas pruebas y por qué_

```
Da un ejemplo
```

## Despliegue 📦

_Agrega notas adicionales sobre como hacer deploy_

## Construido con 🛠️

_Menciona las herramientas que utilizaste para crear tu proyecto_

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - El framework web usado
* [Maven](https://maven.apache.org/) - Manejador de dependencias
* [ROME](https://rometools.github.io/rome/) - Usado para generar RSS

## Contribuyendo 🖇️

Por favor lee el [CONTRIBUTING.md](https://gist.github.com/villanuevand/xxxxxx) para detalles de nuestro código de conducta, y el proceso para enviarnos pull requests.

## Wiki 📖

Puedes encontrar mucho más de cómo utilizar este proyecto en nuestra [Wiki](https://github.com/tu/proyecto/wiki)

## Versionado 📌

Usamos [SemVer](http://semver.org/) para el versionado. Para todas las versiones disponibles, mira los [tags en este repositorio](https://github.com/tu/proyecto/tags).

## Autores ✒️

_Menciona a todos aquellos que ayudaron a levantar el proyecto desde sus inicios_

* **Andrés Villanueva** - *Trabajo Inicial* - [villanuevand](https://github.com/villanuevand)
* **Fulanito Detal** - *Documentación* - [fulanitodetal](#fulanito-de-tal)

También puedes mirar la lista de todos los [contribuyentes](https://github.com/your/project/contributors) quíenes han participado en este proyecto. 

## Licencia 📄

Este proyecto está bajo la Licencia (Tu Licencia) - mira el archivo [LICENSE.md](LICENSE.md) para detalles

## Expresiones de Gratitud 🎁

* Comenta a otros sobre este proyecto 📢
* Invita una cerveza 🍺 o un café ☕ a alguien del equipo. 
* Da las gracias públicamente 🤓.
* Dona con cripto a esta dirección: `0xf253fc233333078436d111175e5a76a649890000`
* etc.



