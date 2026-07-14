try:
    from .tarea import Tarea
    from .heap import MaxHeap
    from .avl import AVL
except ImportError:
    from tarea import Tarea
    from heap import MaxHeap
    from avl import AVL

class SistemaTareas:
    """
    Clase que integra las estructuras MaxHeap y AVL para gestionar las tareas.
    Garantiza que ambas estructuras permanezcan sincronizadas.
    """
    def __init__(self):
        self.heap = MaxHeap()
        self.avl = AVL()

    def agregar_tarea(self, id_tarea, nombre, prioridad):
        """
        Agrega una nueva tarea si el ID no existe en el sistema.
        Retorna True si se agregó con éxito, False si el ID está duplicado.
        """
        # Verificar unicidad del ID usando el AVL (búsqueda en O(log n))
        if self.avl.buscar(id_tarea) is not None:
            return False

        # Crear e insertar la tarea en ambas estructuras
        nueva_tarea = Tarea(id_tarea, nombre, prioridad)
        self.avl.insertar(nueva_tarea)
        self.heap.insertar(nueva_tarea)
        return True

    def buscar_tarea(self, id_tarea):
        """
        Busca una tarea por su ID usando el árbol AVL.
        Retorna el objeto Tarea si existe, None en caso contrario.
        """
        return self.avl.buscar(id_tarea)

    def atender_tarea(self):
        """
        Atiende y elimina la tarea de mayor prioridad.
        Sincroniza la eliminación en el árbol AVL.
        Retorna la tarea atendida, o None si no hay tareas.
        """
        tarea_prioritaria = self.heap.extraer_maximo()
        if tarea_prioritaria is not None:
            # Eliminar del AVL para mantener consistencia
            self.avl.eliminar(tarea_prioritaria.id)
            return tarea_prioritaria
        return None

    def eliminar_tarea(self, id_tarea):
        """
        Elimina una tarea por su ID de ambas estructuras.
        Retorna la tarea eliminada si existía, None en caso contrario.
        """
        # Eliminar del AVL
        tarea_eliminada = self.avl.eliminar(id_tarea)
        if tarea_eliminada is not None:
            # Eliminar del Heap
            self.heap.eliminar_por_id(id_tarea)
            return tarea_eliminada
        return None

    def modificar_prioridad(self, id_tarea, nueva_prioridad):
        """
        Modifica la prioridad de una tarea existente.
        Actualiza y reordena tanto en el AVL como en el Heap.
        Retorna True si se modificó con éxito, False si la tarea no existe.
        """
        tarea = self.avl.buscar(id_tarea)
        if tarea is None:
            return False

        # Actualizar prioridad en el objeto compartido
        tarea.prioridad = nueva_prioridad

        # Re-balancear la cola de prioridad
        self.heap.actualizar_prioridad(id_tarea, nueva_prioridad)
        return True

    def obtener_siguiente_tarea(self):
        """
        Retorna la tarea de mayor prioridad sin atenderla.
        """
        return self.heap.ver_maximo()

    def listar_tareas_por_id(self):
        """
        Retorna una lista de tareas ordenadas ascendentemente por su ID (Inorden AVL).
        """
        return self.avl.inorden()

    def listar_tareas_por_prioridad(self):
        """
        Retorna una lista de tareas ordenadas descendentemente por su prioridad.
        """
        # Se obtiene el listado y se ordena por prioridad de forma descendente
        # En caso de empate en prioridad, opcionalmente se ordena por ID secundario
        tareas = self.avl.inorden()
        return sorted(tareas, key=lambda t: (t.prioridad, -t.id), reverse=True)

    def cantidad_tareas(self):
        """
        Retorna la cantidad total de tareas en el sistema.
        """
        return self.heap.tamano()
