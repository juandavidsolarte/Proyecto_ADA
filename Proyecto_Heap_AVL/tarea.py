class Tarea:
    """
    Clase que representa una tarea individual en el sistema.
    """
    def __init__(self, id, nombre, prioridad):
        self.id = id
        self.nombre = nombre
        self.prioridad = prioridad

    def __str__(self):
        return f"[{self.id}] {self.nombre} (Prioridad: {self.prioridad})"

    def __repr__(self):
        return self.__str__()
