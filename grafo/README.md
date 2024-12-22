- Titulo: Integrantes, descripcion, proyecto. | Carlos
- Contexto: Uso de simpy, Simulacion discreta de agentes. | Dani
- agentes.py : Explicar agentes, metodos importantes y contexto de atributos | Cleme
- func_param.py : *** | Carlos
- input_auto.py : Explicar como se forman estos inputs, funciones mas importantes. | Basti
- manager.py : Explicar en conjunto con E/R, funcionamiento como tal, y metodos importantes. | Cleme
- main.py : instrucciones, parametros. | Carlos
- visual.py : explicar visualizacion actual, instrucciones. | Basti

# Título del Proyecto

_Acá va un párrafo que describa lo que es el proyecto_

## Comenzando 🚀

_Estas instrucciones te permitirán obtener una copia del proyecto en funcionamiento en tu máquina local para propósitos de desarrollo y pruebas._

Mira **Deployment** para conocer como desplegar el proyecto.



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

En la carpeta [visual](/visual) se encuentran todas los archivos 
correspondientes al apartado visual de esta simulación

**Consideraciones**: No esta integrada la visualización del todo con la simulación creada en este proyecto, la visualización esta basada en el output que retorna nuestra simulación,
esto se puede generalizar, la idea de la visualización es dar un primer paso para que la empresa pueda crear una visualización del apartado maritimo
si así lo desean adaptando el output de la simulación que ellos generen y escalando el codigo de la visualización.

Funcionamiento de la visualización: Se compone principalmente de 3 archivos

- [input_visual.py](/visual/input_visual.py)
- [visual.py](/visual/visual.py)
- [run.py](/visual/run.py)

















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



