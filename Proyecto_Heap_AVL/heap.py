class MaxHeap:
    """
    Clase que implementa una cola de prioridad basada en un Max Heap.
    Las tareas se ordenan según su prioridad.
    """
    def __init__(self):
        self.heap = []

    def mostrar(self):
        for tarea in self.heap:
            print(tarea)

    def insertar(self, tarea):
        """
        Inserta una nueva tarea en el Max Heap.
        """
        # Agregar la tarea al final de la lista
        self.heap.append(tarea)

        # Restaurar la propiedad del Max Heap
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, indice):
        """
        Restaura la propiedad del Max Heap moviendo un elemento hacia arriba.
        """
        while indice > 0:
            padre = (indice - 1) // 2
            if self.heap[indice].prioridad > self.heap[padre].prioridad:
                self.heap[indice], self.heap[padre] = (
                    self.heap[padre],
                    self.heap[indice]
                )
                indice = padre
            else:
                break

    def extraer_maximo(self):
        """
        Elimina y retorna la tarea con mayor prioridad.
        """
        # Verificar si el heap está vacío
        if len(self.heap) == 0:
            return None

        # Guardar el elemento de la raíz
        maximo = self.heap[0]

        # Si solo hay un elemento, hacer pop y retornar
        if len(self.heap) == 1:
            return self.heap.pop()

        # Mover el último elemento a la raíz
        self.heap[0] = self.heap[-1]

        # Eliminar el último elemento
        self.heap.pop()

        # Restaurar la propiedad del heap
        if len(self.heap) > 0:
            self.heapify_down(0)

        return maximo

    def heapify_down(self, indice):
        """
        Restaura la propiedad del Max Heap moviendo un elemento hacia abajo.
        """
        while True:
            mayor = indice
            izquierdo = 2 * indice + 1
            derecho = 2 * indice + 2

            # Comparar con el hijo izquierdo
            if (izquierdo < len(self.heap) and
                self.heap[izquierdo].prioridad > self.heap[mayor].prioridad):
                mayor = izquierdo

            # Comparar con el hijo derecho
            if (derecho < len(self.heap) and
                self.heap[derecho].prioridad > self.heap[mayor].prioridad):
                mayor = derecho

            # Si el mayor sigue siendo el padre, terminamos
            if mayor == indice:
                break

            # Intercambiar
            self.heap[indice], self.heap[mayor] = (
                self.heap[mayor],
                self.heap[indice]
            )

            # Continuar desde la nueva posición
            indice = mayor

    def esta_vacio(self):
        """
        Retorna True si el Heap está vacío, de lo contrario False.
        """
        return len(self.heap) == 0

    def ver_maximo(self):
        """
        Retorna la tarea de mayor prioridad sin removerla.
        """
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def tamano(self):
        """
        Retorna el número de elementos en el heap.
        """
        return len(self.heap)

    def eliminar_por_id(self, id_tarea):
        """
        Busca y elimina una tarea del heap según su ID.
        Retorna la tarea eliminada, o None si no se encuentra.
        """
        indice = -1
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                indice = i
                break

        if indice == -1:
            return None

        tarea_eliminada = self.heap[indice]
        # Si es el último elemento
        if indice == len(self.heap) - 1:
            self.heap.pop()
            return tarea_eliminada

        # Intercambiar con el último elemento y eliminar el último
        self.heap[indice] = self.heap[-1]
        self.heap.pop()

        # Restaurar propiedad del Heap en el índice modificado
        self.heapify_up(indice)
        self.heapify_down(indice)

        return tarea_eliminada

    def actualizar_prioridad(self, id_tarea, nueva_prioridad):
        """
        Actualiza la prioridad de una tarea en el heap.
        Retorna True si se actualizó con éxito, de lo contrario False.
        """
        indice = -1
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                indice = i
                break

        if indice == -1:
            return False

        self.heap[indice].prioridad = nueva_prioridad
        # Re-organizar la posición del elemento modificado
        self.heapify_up(indice)
        self.heapify_down(indice)
        return True
