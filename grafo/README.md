- Titulo: Integrantes, descripcion, proyecto. | Carlos
- Contexto: Uso de simpy, Simulacion discreta de agentes. | Dani
- agentes.py : Explicar agentes, metodos importantes y contexto de atributos | Cleme
- func_param.py : *** | Carlos
- input_auto.py : Explicar como se forman estos inputs, funciones mas importantes. | Basti
- manager.py : Explicar en conjunto con E/R, funcionamiento como tal, y metodos importantes. | Cleme
- main.py : instrucciones, parametros. | Carlos
- visual.py : explicar visualizacion actual, instrucciones. | Basti

# Simulacion Maritima 

Integrantes: - Clemente Campos
             - Carlos Olguin
             - Felipe Cox
             - Daniel Hidalgo
             - Bastian Cortés

Descripción: El siguiente repo contiene instrucciones y documentacion en torno a la solución planteada por el equipo en torno a la problematica de tener un simulador maritimo, para esto fue documentado los archivos necesarios en conjunto a todo lo necesario para entender el como se corre el codigo y su funcionamiento.

## Contexto

Este proyecto emplea como base para la modelación del comercio marítimo internacional tanto el paradigma de simulación basada en agentes
como el paradigma de simulación de eventos discretos. Hemos diseñado tres clases diferentes para crear los barcos, puertos y rutas, que
son los agentes clave en el modelo, y hemos utilizado SimPy, que es una librería de Python que nos permitió simular eventos en tiempo
discreto. Con esta librería creamos una simulación del comercio marítimo internacional con un enfoque que permite representar cada 
barco, puerto y ruta como agentes con comportamientos y características definidas, que interactúan en un entorno dinámico. La simulación
captura eventos clave del comercio marítimo como el movimiento de los barcos entre los distintos puertos, además del cierre y apertura 
temporal de puertos y de rutas, con las respectivas consecuencias que generan dichos eventos en el sistema.

### Input Automático ⚙️

En el archivo [input_auto.py](clases/input_auto.py) se generan 
aleatoreamente los agentes de la simulación a partir de un numero 
de puertos como input, las distribuciones que se usaron para la 
aleatoriedad fueron uniformes por simplicidad, siempre
pensando en que puede ser esto modificado dependiendo del proposito
de la empresa. El funcionamiento es el siguiente:

- generate_agents: Función que se encarga de generar todos los agentes
llamando a otras funciones y finalmente retorna diccionarios con instancias
de las clases (clases definidas en [agentes.py](/grafo/clases/agentes.py)) más
una matriz de adyacencia de las distancias entre rutas 
    - El numero de barcos generados se escoge aleatoriamente entre 1 y 
    la capacidad maxima global que pueden almacenar los puertos 
    - También posee un argumento debug el cual por defecto esta en falso
    si lo ponemos en True se generara un archivo debug.txt el cual retorna
    la información de todas las entidades generadas

- gen_ports: Dado un número de puertos genera un diccionario con los puertos 
aleatorios de la clase [Port](/grafo/clases/agentes.py#L78), además retorna la
suma de todas las capacidades de los puertos
    - La capacidad maxima de un puerto individual es un numero aleatorio entre 1 y 50

- all_routes: Recibe el número de puertos que se quieren generar, retorna una lista
con todas las tuplas que representen rutas posibles en la simulación.
    - Podrian existir más rutas de las que generamos, eso es algo que se 
    puede generalizar a partir de nuestro codigo

- gen_ships: Dado un número de barcos (escogido en generate_agents), un numero de puertos y una lista con todas las rutas posibles entre puertos se genera un diccionario
con los barcos aleatorios de la clase [Ship](/grafo/clases/agentes.py#L5),
se asume un id secuencial (0,1,...,num_ships-1), la carga y la velocidad
se generan con ciertas funciones basadas en distribuciones uniformes (ver el punto Otros)
además se genera el itinerario con la función gen_itinerary y retorna el diccionario con los barcos y las rutas usadas por los barcos.
    - Acá asumimos que solo van a existir las rutas que se escogieron al azar
    es claro que también uno poddria considerar más rutas, se puede genralizar.

- gen_itinerary: Recibe un numero aleatorio de las tareas que debe realizar el
barco (generado en gen_ships), id del puerto inicial,si es ciclico el barco y un set de las rutas que
ya se han utilizado, a partir del id inciial se genera aleatoreamente el id del 
siguiente puerto destino y se agrega al itinerario hasta llenar el itinerario.

- gen_route: Recibe las rutas que se usaron,  itera por estas rutas y genera su información
la distancia se genera escogiendo puntos aleatorios en la tierra (latitudes, longuitudes aleatorias)
y calculando su distancia con la función gen_dist

- gen_random_point: Genera una latitud y longuitud aleatoria

- gen_dist: recibe el id inicial y final de una ruta, mas los puntos ya generados a las distintos
puertos, se verifica no volver a generar un punto aleatorio a un puerto que ya se le habia genrado uno
retorna la distancia geodesica utilizando la libreria geopy
    - Hay muchas otras formas de calcular la distancia, se puede generalizar dependiendo del proposito.

- gen_matrix: Dado el numero de puertos y clases de rutas se genera la matriz de adyacencia de la simulacion
la cual tendra las distancias de las rutas

- Otros: También hay otras funciones como [gen_velocity](/grafo/clases/input_auto.py#L257) las cuales están pensadas para agregar mayor dinamica o funcionamineto
al código, se ubican al final del código del archivo.

### Visualización 🗺️

![](/visual/simulation.gif)

En la carpeta [visual](/visual) se encuentran todas los archivos 
correspondientes al apartado visual de esta simulación

**Consideraciones**: No esta integrada la visualización del todo con la simulación creada en este proyecto, la visualización esta basada en el output que retorna nuestra simulación,
esto se puede generalizar, la idea de la visualización es dar un primer paso para que la empresa pueda crear una visualización del apartado maritimo
si así lo desean adaptando el output de la simulación que ellos generen y escalando el codigo de la visualización.

Funcionamiento de la visualización: Se compone principalmente de 3 archivos

- [input_visual.py](/visual/input_visual.py): En este archivo se encuentra la función [load_simulation](/visual/input_visual.py#L1) que carga
un archivo.txt, el archivo.txt que maneja tiene el siguiente formato
    - Se ha implementado el movimineto de los barcos, la función load_simulation es independiente
    de t, las lineas que contienen t son para mejor entendimiento del input.

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
         
        - [get_shortest_path](/visual/visual.py#L118): En esta función se utiliza la libreria de searoute, en particular la función searoute la cual recibe las coordenadas de dos puntos de la tierra y retorna una objeto especial con la informacion de la ruta mas corta maritima del cual extraemos una lista de las coordenadas de esta ruta, además añadimos
        al mapa (esta en el atributo self.map, objeto de folium) una interpolación de esta ruta
        
        - [add_feature](/visual/visual.py#L186): recibe la infromacion de un objeto que tenga
        movimiento y lo agrega a la lista self.features, se podrian agregar mas entidades
        con movimiento usando esta función, para este proyecto solamente maneja el movimiento de los barcos
        
        - [run](/visual/visual.py#L220): En esta función se añaden los marcadores (los iconos
        de los puertos en este proyecto) con la función self.add_markers, además se utiliza el
        plugin de folium TimestampedGeoJson el cual es el encargado de manejar el movimiento de 
        los barcos en la visualización.

    - [create_simulation](/visual/visual.py#L260): Recibe diccionarios con la informacion de los
    el tiempo de la simulación (cuantos intervalos se van a realizar), tipo de mapa, y
    una ruta de donde se guardara el archivo .html. En esta función se crea la instancia
    Map de folium, la cual es la que posee el mapa que se vera en la visualización, 
    inicializamos la clase Visual, añadimos la información de los agentes a la clase
    y luego ejecutamos metodos de la clase para hacer que todo funcione y retornar la output .html.


- [run.py](/visual/run.py): En este archivo se ejecuta la visualización, se crean los parametros,
se obtienen los agentes y se ejecuta la visualización con la funcción create_simulation.


### Ejecución 📋















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



