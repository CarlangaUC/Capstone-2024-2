from clases.clases import Manager

manager = Manager()
manager.add("ports.txt", "routes.txt", "ships.txt")
manager.processes([0, 1, 2])
manager.run(15)
