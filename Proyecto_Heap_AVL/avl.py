class NodoAVL:
    """
    Representa un nodo en el Árbol AVL.
    Almacena una tarea y se indexa por su ID único.
    """
    def __init__(self, tarea):
        self.tarea = tarea
        self.id = tarea.id
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class AVL:
    """
    Implementación de un Árbol AVL (Árbol Binario de Búsqueda Auto-Balanceado).
    Las tareas se organizan en base a su ID.
    """
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        """
        Retorna la altura de un nodo. Retorna 0 si es None.
        """
        if nodo is None:
            return 0
        return nodo.altura

    def actualizar_altura(self, nodo):
        """
        Recalcula la altura de un nodo basándose en la altura de sus hijos.
        """
        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierdo),
            self.obtener_altura(nodo.derecho)
        )

    def factor_balance(self, nodo):
        """
        Calcula el factor de balance de un nodo.
        """
        if nodo is None:
            return 0
        return (
            self.obtener_altura(nodo.izquierdo)
            - self.obtener_altura(nodo.derecho)
        )

    def rotacion_derecha(self, y):
        """
        Realiza una rotación simple a la derecha para rebalancear un subárbol.
        """
        x = y.izquierdo
        T2 = x.derecho

        # Rotación
        x.derecho = y
        y.izquierdo = T2

        # Actualizar alturas
        self.actualizar_altura(y)
        self.actualizar_altura(x)

        return x

    def rotacion_izquierda(self, x):
        """
        Realiza una rotación simple a la izquierda para rebalancear un subárbol.
        """
        y = x.derecho
        T2 = y.izquierdo

        # Rotación
        y.izquierdo = x
        x.derecho = T2

        # Actualizar alturas
        self.actualizar_altura(x)
        self.actualizar_altura(y)

        return y

    def insertar(self, tarea):
        """
        Inserta una tarea en el árbol AVL.
        """
        self.raiz = self._insertar(self.raiz, tarea)

    def _insertar(self, nodo, tarea):
        # 1. Inserción estándar de BST
        if nodo is None:
            return NodoAVL(tarea)

        if tarea.id < nodo.id:
            nodo.izquierdo = self._insertar(nodo.izquierdo, tarea)
        elif tarea.id > nodo.id:
            nodo.derecho = self._insertar(nodo.derecho, tarea)
        else:
            # Si el ID ya existe, no se permite duplicado en el árbol
            return nodo

        # 2. Actualizar altura de este nodo ancestro
        self.actualizar_altura(nodo)

        # 3. Obtener el factor de balance
        balance = self.factor_balance(nodo)

        # Casos de desbalanceo

        # Caso Izquierda-Izquierda (LL)
        if balance > 1 and tarea.id < nodo.izquierdo.id:
            return self.rotacion_derecha(nodo)

        # Caso Derecha-Derecha (RR)
        if balance < -1 and tarea.id > nodo.derecho.id:
            return self.rotacion_izquierda(nodo)

        # Caso Izquierda-Derecha (LR)
        if balance > 1 and tarea.id > nodo.izquierdo.id:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)

        # Caso Derecha-Izquierda (RL)
        if balance < -1 and tarea.id < nodo.derecho.id:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    def buscar(self, id_tarea):
        """
        Busca una tarea en el árbol AVL por su ID.
        Retorna el objeto Tarea si existe, None en caso contrario.
        """
        return self._buscar(self.raiz, id_tarea)

    def _buscar(self, nodo, id_tarea):
        if nodo is None:
            return None

        if id_tarea == nodo.id:
            return nodo.tarea
        elif id_tarea < nodo.id:
            return self._buscar(nodo.izquierdo, id_tarea)
        else:
            return self._buscar(nodo.derecho, id_tarea)

    def eliminar(self, id_tarea):
        """
        Elimina la tarea con el ID especificado del árbol AVL.
        Retorna la tarea eliminada si existía, o None.
        """
        self.raiz, tarea_eliminada = self._eliminar(self.raiz, id_tarea)
        return tarea_eliminada

    def _eliminar(self, nodo, id_tarea):
        if nodo is None:
            return None, None

        tarea_eliminada = None

        if id_tarea < nodo.id:
            nodo.izquierdo, tarea_eliminada = self._eliminar(nodo.izquierdo, id_tarea)
        elif id_tarea > nodo.id:
            nodo.derecho, tarea_eliminada = self._eliminar(nodo.derecho, id_tarea)
        else:
            # Encontrado el nodo a eliminar
            tarea_eliminada = nodo.tarea

            # Caso 1 o 0 hijos
            if nodo.izquierdo is None:
                return nodo.derecho, tarea_eliminada
            elif nodo.derecho is None:
                return nodo.izquierdo, tarea_eliminada

            # Caso 2 hijos: Obtener el sucesor inorden (el mínimo del subárbol derecho)
            sucesor = self._obtener_minimo(nodo.derecho)
            nodo.id = sucesor.id
            nodo.tarea = sucesor.tarea
            nodo.derecho, _ = self._eliminar(nodo.derecho, sucesor.id)

        if nodo is None:
            return None, tarea_eliminada

        # Actualizar altura de este nodo
        self.actualizar_altura(nodo)

        # Calcular factor de balance
        balance = self.factor_balance(nodo)

        # Rebalancear el subárbol

        # Caso LL
        if balance > 1 and self.factor_balance(nodo.izquierdo) >= 0:
            return self.rotacion_derecha(nodo), tarea_eliminada

        # Caso LR
        if balance > 1 and self.factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo), tarea_eliminada

        # Caso RR
        if balance < -1 and self.factor_balance(nodo.derecho) <= 0:
            return self.rotacion_izquierda(nodo), tarea_eliminada

        # Caso RL
        if balance < -1 and self.factor_balance(nodo.derecho) > 0:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo), tarea_eliminada

        return nodo, tarea_eliminada

    def _obtener_minimo(self, nodo):
        actual = nodo
        while actual.izquierdo is not None:
            actual = actual.izquierdo
        return actual

    def inorden(self):
        """
        Retorna una lista de tareas ordenadas ascendentemente por su ID.
        """
        tareas = []
        self._inorden(self.raiz, tareas)
        return tareas

    def _inorden(self, nodo, lista):
        if nodo is not None:
            self._inorden(nodo.izquierdo, lista)
            lista.append(nodo.tarea)
            self._inorden(nodo.derecho, lista)
