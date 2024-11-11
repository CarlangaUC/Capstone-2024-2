from collections import namedtuple
from clases.clases import Manager

#Event = namedtuple("Event", ["final_port_id", "load"])

manager = Manager()
manager.add("ports.txt", "routes.txt", "ships.txt")
manager.processes()
manager.run(50)
