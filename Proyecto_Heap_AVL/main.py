import tkinter as tk
from tkinter import messagebox, ttk

# =====================================================================
# 1. CLASES DE ESTRUCTURAS DE DATOS (Árbol AVL & MaxHeap)
# =====================================================================

class Tarea:
    """Clase que representa una Tarea individual."""
    def __init__(self, id, nombre, prioridad):
        self.id = id
        self.nombre = nombre
        self.prioridad = prioridad

    def __str__(self):
        return f"[{self.id}] {self.nombre} (Prioridad: {self.prioridad})"

    def __repr__(self):
        return self.__str__()


class NodoAVL:
    """Nodo del Árbol AVL que almacena un objeto Tarea."""
    def __init__(self, tarea):
        self.tarea = tarea
        self.id = tarea.id
        self.izquierdo = None
        self.derecho = None
        self.altura = 1


class AVL:
    """Árbol Binario de Búsqueda Auto-balanceado (AVL) ordenado por ID."""
    def __init__(self):
        self.raiz = None

    def obtener_altura(self, nodo):
        if nodo is None:
            return 0
        return nodo.altura

    def actualizar_altura(self, nodo):
        nodo.altura = 1 + max(
            self.obtener_altura(nodo.izquierdo),
            self.obtener_altura(nodo.derecho)
        )

    def factor_balance(self, nodo):
        if nodo is None:
            return 0
        return self.obtener_altura(nodo.izquierdo) - self.obtener_altura(nodo.derecho)

    def rotacion_derecha(self, y):
        x = y.izquierdo
        T2 = x.derecho
        x.derecho = y
        y.izquierdo = T2
        self.actualizar_altura(y)
        self.actualizar_altura(x)
        return x

    def rotacion_izquierda(self, x):
        y = x.derecho
        T2 = y.izquierdo
        y.izquierdo = x
        x.derecho = T2
        self.actualizar_altura(x)
        self.actualizar_altura(y)
        return y

    def insertar(self, tarea):
        self.raiz = self._insertar(self.raiz, tarea)

    def _insertar(self, nodo, tarea):
        if nodo is None:
            return NodoAVL(tarea)

        if tarea.id < nodo.id:
            nodo.izquierdo = self._insertar(nodo.izquierdo, tarea)
        elif tarea.id > nodo.id:
            nodo.derecho = self._insertar(nodo.derecho, tarea)
        else:
            return nodo  # No se permiten duplicados de ID

        self.actualizar_altura(nodo)
        balance = self.factor_balance(nodo)

        # Casos de desbalanceo
        if balance > 1 and tarea.id < nodo.izquierdo.id:
            return self.rotacion_derecha(nodo)
        if balance < -1 and tarea.id > nodo.derecho.id:
            return self.rotacion_izquierda(nodo)
        if balance > 1 and tarea.id > nodo.izquierdo.id:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo)
        if balance < -1 and tarea.id < nodo.derecho.id:
            nodo.derecho = self.rotacion_derecha(nodo.derecho)
            return self.rotacion_izquierda(nodo)

        return nodo

    def buscar(self, id_tarea):
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
            tarea_eliminada = nodo.tarea
            if nodo.izquierdo is None:
                return nodo.derecho, tarea_eliminada
            elif nodo.derecho is None:
                return nodo.izquierdo, tarea_eliminada

            sucesor = self._obtener_minimo(nodo.derecho)
            nodo.id = sucesor.id
            nodo.tarea = sucesor.tarea
            nodo.derecho, _ = self._eliminar(nodo.derecho, sucesor.id)

        if nodo is None:
            return None, tarea_eliminada

        self.actualizar_altura(nodo)
        balance = self.factor_balance(nodo)

        # Re-balanceo tras eliminar
        if balance > 1 and self.factor_balance(nodo.izquierdo) >= 0:
            return self.rotacion_derecha(nodo), tarea_eliminada
        if balance > 1 and self.factor_balance(nodo.izquierdo) < 0:
            nodo.izquierdo = self.rotacion_izquierda(nodo.izquierdo)
            return self.rotacion_derecha(nodo), tarea_eliminada
        if balance < -1 and self.factor_balance(nodo.derecho) <= 0:
            return self.rotacion_izquierda(nodo), tarea_eliminada
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
        tareas = []
        self._inorden(self.raiz, tareas)
        return tareas

    def _inorden(self, nodo, lista):
        if nodo is not None:
            self._inorden(nodo.izquierdo, lista)
            lista.append(nodo.tarea)
            self._inorden(nodo.derecho, lista)


class MaxHeap:
    """Cola de Prioridad MaxHeap basada en la prioridad de la Tarea."""
    def __init__(self):
        self.heap = []

    def insertar(self, tarea):
        self.heap.append(tarea)
        self.heapify_up(len(self.heap) - 1)

    def heapify_up(self, indice):
        while indice > 0:
            padre = (indice - 1) // 2
            if self.heap[indice].prioridad > self.heap[padre].prioridad:
                self.heap[indice], self.heap[padre] = self.heap[padre], self.heap[indice]
                indice = padre
            else:
                break

    def extraer_maximo(self):
        if len(self.heap) == 0:
            return None
        maximo = self.heap[0]
        if len(self.heap) == 1:
            return self.heap.pop()
        self.heap[0] = self.heap[-1]
        self.heap.pop()
        if len(self.heap) > 0:
            self.heapify_down(0)
        return maximo

    def heapify_down(self, indice):
        while True:
            mayor = indice
            izquierdo = 2 * indice + 1
            derecho = 2 * indice + 2

            if izquierdo < len(self.heap) and self.heap[izquierdo].prioridad > self.heap[mayor].prioridad:
                mayor = izquierdo
            if derecho < len(self.heap) and self.heap[derecho].prioridad > self.heap[mayor].prioridad:
                mayor = derecho

            if mayor == indice:
                break
            self.heap[indice], self.heap[mayor] = self.heap[mayor], self.heap[indice]
            indice = mayor

    def esta_vacio(self):
        return len(self.heap) == 0

    def ver_maximo(self):
        if len(self.heap) == 0:
            return None
        return self.heap[0]

    def tamano(self):
        return len(self.heap)

    def eliminar_por_id(self, id_tarea):
        indice = -1
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                indice = i
                break

        if indice == -1:
            return None

        tarea_eliminada = self.heap[indice]
        if indice == len(self.heap) - 1:
            self.heap.pop()
            return tarea_eliminada

        self.heap[indice] = self.heap[-1]
        self.heap.pop()
        self.heapify_up(indice)
        self.heapify_down(indice)
        return tarea_eliminada

    def actualizar_prioridad(self, id_tarea, nueva_prioridad):
        indice = -1
        for i, tarea in enumerate(self.heap):
            if tarea.id == id_tarea:
                indice = i
                break

        if indice == -1:
            return False

        self.heap[indice].prioridad = nueva_prioridad
        self.heapify_up(indice)
        self.heapify_down(indice)
        return True


# =====================================================================
# 2. SISTEMA INTEGRADO (Orquestador de estructuras)
# =====================================================================

class SistemaTareas:
    """Controlador que vincula el AVL y el MaxHeap."""
    def __init__(self):
        self.heap = MaxHeap()
        self.avl = AVL()

    def agregar_tarea(self, id_tarea, nombre, prioridad):
        if self.avl.buscar(id_tarea) is not None:
            return False
        nueva_tarea = Tarea(id_tarea, nombre, prioridad)
        self.avl.insertar(nueva_tarea)
        self.heap.insertar(nueva_tarea)
        return True

    def buscar_tarea(self, id_tarea):
        return self.avl.buscar(id_tarea)

    def atender_tarea(self):
        tarea_prioritaria = self.heap.extraer_maximo()
        if tarea_prioritaria is not None:
            self.avl.eliminar(tarea_prioritaria.id)
            return tarea_prioritaria
        return None

    def eliminar_tarea(self, id_tarea):
        tarea_eliminada = self.avl.eliminar(id_tarea)
        if tarea_eliminada is not None:
            self.heap.eliminar_por_id(id_tarea)
            return tarea_eliminada
        return None

    def completar_tarea(self, id_tarea):
        return self.eliminar_tarea(id_tarea)

    def modificar_prioridad(self, id_tarea, nueva_prioridad):
        tarea = self.avl.buscar(id_tarea)
        if tarea is None:
            return False
        tarea.prioridad = nueva_prioridad
        self.heap.actualizar_prioridad(id_tarea, nueva_prioridad)
        return True

    def obtener_siguiente_tarea(self):
        return self.heap.ver_maximo()

    def listar_tareas_por_id(self):
        return self.avl.inorden()

    def listar_tareas_por_prioridad(self):
        # Mantiene el orden de prioridad de forma descendente estable
        tareas = self.avl.inorden()
        return sorted(tareas, key=lambda t: (t.prioridad, -t.id), reverse=True)

    def cantidad_tareas(self):
        return self.heap.tamano()


# =====================================================================
# 3. CLASE INTERFAZ GRÁFICA (GUI con banner retro incorporado)
# =====================================================================

class SistemaTareasGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas Inteligente")
        self.root.geometry("920x720")
        self.root.minsize(850, 600)
        
        # Inicializar el motor del sistema
        self.sistema = SistemaTareas()
        self.cargar_datos_prueba()

        # Configurar estilos de Tkinter
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Estilos visuales
        self.style.configure('.', font=('Helvetica', 10))
        self.style.configure('TButton', font=('Helvetica', 10, 'bold'), borderwidth=1)
        self.style.configure('Action.TButton', background='#17A2B8', foreground='white')
        self.style.map('Action.TButton', background=[('active', '#138496')])

        self.crear_widgets()
        self.actualizar_tablas()

    def cargar_datos_prueba(self):
        # Tareas iniciales de demostración
        self.sistema.agregar_tarea(101, "Estudiar para el examen final", 11)
        self.sistema.agregar_tarea(102, "Comprar insumos escolares", 5)
        self.sistema.agregar_tarea(103, "Revisar correos importantes", 10)
        self.sistema.agregar_tarea(104, "Preparar la cena familiar", 7)
        self.sistema.agregar_tarea(105, "Sacar a pasear a la mascota", 9)

    def crear_widgets(self):
        # --- PANEL CONTENEDOR PRINCIPAL ---
        main_frame = ttk.Frame(self.root, padding=15)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # =====================================================================
        # DISEÑO DEL LOGO/BANNER RETRO
        # =====================================================================
        # Lienzo oscuro para albergar el diseño retro
        self.banner_frame = tk.Frame(main_frame, bg="#121212", relief="ridge", bd=3)
        self.banner_frame.pack(fill=tk.X, pady=(0, 15))

        # Texto del logo ASCII recreado
        texto_logo = (
            "██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗ ██████╗████████╗ ██████╗ \n"
            "██╔══██╗██╔══██╗██╔═══██╗╚██╗ ██╔╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗\n"
            "██████╔╝██████╔╝██║   ██║ ╚████╔╝ █████╗  ██║        ██║   ██║   ██║\n"
            "██╔═══╝ ██╔══██╗██║   ██║  ╚██╔╝  ██╔══╝  ██║        ██║   ██║   ██║\n"
            "██║     ██║  ██║╚██████╔╝   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝\n"
            "╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ "
        )

        # Dibujar el logo en el canvas retro (Cian brillante)
        lbl_logo = tk.Label(
            self.banner_frame, 
            text=texto_logo, 
            font=("Courier New", 8, "bold"), 
            bg="#121212", 
            fg="#00E5FF", 
            justify="center"
        )
        lbl_logo.pack(pady=(10, 2))

        # Subtítulo 1: SISTEMA DE GESTIÓN DE TAREAS (Amarillo brillante)
        lbl_sub_1 = tk.Label(
            self.banner_frame, 
            text="S I S T E M A   D E   G E S T I O N   D E   T A R E A S", 
            font=("Consolas", 12, "bold"), 
            bg="#121212", 
            fg="#FFD700"
        )
        lbl_sub_1.pack(pady=2)

        # Subtítulo 2: (MaxHeap + Árbol AVL) (Violeta/Fucsia brillante)
        lbl_sub_2 = tk.Label(
            self.banner_frame, 
            text="(MaxHeap + Árbol AVL)", 
            font=("Consolas", 11, "bold"), 
            bg="#121212", 
            fg="#FF00FF"
        )
        lbl_sub_2.pack(pady=(0, 10))

        # =====================================================================
        # PANEL DEL CUERPO (Control izquierdo y Datos a la derecha)
        # =====================================================================
        body_frame = ttk.Frame(main_frame)
        body_frame.pack(fill=tk.BOTH, expand=True)

        # Lateral izquierdo
        left_panel = ttk.Frame(body_frame, width=325)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
        left_panel.pack_propagate(False)

        # Cuerpo derecho
        right_panel = ttk.Frame(body_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # --- SECCIÓN A: AGREGAR NUEVAS TAREAS ---
        add_lf = ttk.LabelFrame(left_panel, text=" Crear Nueva Tarea ", padding=10)
        add_lf.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(add_lf, text="ID único (Entero):").grid(row=0, column=0, sticky='w', pady=2)
        self.ent_id = ttk.Entry(add_lf)
        # CORREGIDO: Se cambia "fill=tk.X" por "sticky='ew'" para evitar el error de grid
        self.ent_id.grid(row=0, column=1, sticky='ew', pady=2, padx=(5, 0))

        ttk.Label(add_lf, text="Descripción:").grid(row=1, column=0, sticky='w', pady=2)
        self.ent_nombre = ttk.Entry(add_lf)
        # CORREGIDO: Se cambia "fill=tk.X" por "sticky='ew'" para evitar el error de grid
        self.ent_nombre.grid(row=1, column=1, sticky='ew', pady=2, padx=(5, 0))

        ttk.Label(add_lf, text="Prioridad:").grid(row=2, column=0, sticky='w', pady=2)
        self.ent_prioridad = ttk.Entry(add_lf)
        # CORREGIDO: Se cambia "fill=tk.X" por "sticky='ew'" para evitar el error de grid
        self.ent_prioridad.grid(row=2, column=1, sticky='ew', pady=2, padx=(5, 0))

        btn_agregar = ttk.Button(add_lf, text="Añadir al Sistema", style='Action.TButton', command=self.agregar_tarea)
        btn_agregar.grid(row=3, column=0, columnspan=2, pady=(8, 0), sticky='ew')

        add_lf.columnconfigure(1, weight=1)

        # --- SECCIÓN B: CONTROLES DE ACCIÓN ---
        actions_lf = ttk.LabelFrame(left_panel, text=" Panel de Control y Modificaciones ", padding=10)
        actions_lf.pack(fill=tk.BOTH, expand=True)

        # Atender la prioritaria de inmediato
        btn_atender = ttk.Button(actions_lf, text="⭐ Atender Siguiente Tarea (Max)", command=self.atender_tarea)
        btn_atender.pack(fill=tk.X, pady=5)

        ttk.Separator(actions_lf, orient='horizontal').pack(fill=tk.X, pady=8)

        # Entrada ID para interactuar
        ttk.Label(actions_lf, text="ID de Tarea Seleccionada:").pack(anchor='w')
        self.ent_id_accion = ttk.Entry(actions_lf)
        self.ent_id_accion.pack(fill=tk.X, pady=2)

        # Modificación de Prioridad
        mod_frame = ttk.Frame(actions_lf)
        mod_frame.pack(fill=tk.X, pady=(5, 2))
        ttk.Label(mod_frame, text="Nueva Prioridad:").pack(side=tk.LEFT)
        self.ent_nueva_prioridad = ttk.Entry(mod_frame, width=10)
        self.ent_nueva_prioridad.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))

        btn_modificar = ttk.Button(actions_lf, text="Actualizar Prioridad", command=self.modificar_prioridad)
        btn_modificar.pack(fill=tk.X, pady=2)

        ttk.Separator(actions_lf, orient='horizontal').pack(fill=tk.X, pady=8)

        # Buscar / Completar (Eliminar)
        btn_buscar = ttk.Button(actions_lf, text="Buscar Tarea en AVL", command=self.buscar_tarea)
        btn_buscar.pack(fill=tk.X, pady=2)

        btn_eliminar = ttk.Button(actions_lf, text="Eliminar / Marcar como Completada", command=self.eliminar_tarea)
        btn_eliminar.pack(fill=tk.X, pady=2)

        # Indicador de conteo actual
        self.lbl_contador = ttk.Label(actions_lf, text="Tareas activas: 5", font=('Helvetica', 10, 'italic'), foreground='#666')
        self.lbl_contador.pack(side=tk.BOTTOM, pady=(10, 0))

        # =====================================================================
        # PESTAÑAS DE VISUALIZACIÓN DE DATOS (Panel Derecho)
        # =====================================================================
        self.notebook = ttk.Notebook(right_panel)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Vista AVL
        self.tab_avl = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_avl, text=" Orden por ID (Estructura AVL) ")
        self.crear_tabla_avl()

        # Vista Heap
        self.tab_heap = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_heap, text=" Orden por Prioridad (Estructura Heap) ")
        self.crear_tabla_heap()

    def crear_tabla_avl(self):
        columnas = ('id', 'nombre', 'prioridad')
        self.tree_avl = ttk.Treeview(self.tab_avl, columns=columnas, show='headings')
        
        self.tree_avl.heading('id', text='ID Tarea')
        self.tree_avl.heading('nombre', text='Nombre de la Tarea')
        self.tree_avl.heading('prioridad', text='Grado de Prioridad')

        self.tree_avl.column('id', width=100, anchor='center')
        self.tree_avl.column('nombre', width=320, anchor='w')
        self.tree_avl.column('prioridad', width=120, anchor='center')

        vsb = ttk.Scrollbar(self.tab_avl, orient="vertical", command=self.tree_avl.yview)
        self.tree_avl.configure(yscrollcommand=vsb.set)

        self.tree_avl.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_avl.bind('<<TreeviewSelect>>', self.al_seleccionar_tarea)

    def crear_tabla_heap(self):
        columnas = ('id', 'nombre', 'prioridad')
        self.tree_heap = ttk.Treeview(self.tab_heap, columns=columnas, show='headings')
        
        self.tree_heap.heading('id', text='ID Tarea')
        self.tree_heap.heading('nombre', text='Nombre de la Tarea')
        self.tree_heap.heading('prioridad', text='Grado de Prioridad')

        self.tree_heap.column('id', width=100, anchor='center')
        self.tree_heap.column('nombre', width=320, anchor='w')
        self.tree_heap.column('prioridad', width=120, anchor='center')

        vsb = ttk.Scrollbar(self.tab_heap, orient="vertical", command=self.tree_heap.yview)
        self.tree_heap.configure(yscrollcommand=vsb.set)

        self.tree_heap.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree_heap.bind('<<TreeviewSelect>>', self.al_seleccionar_tarea)

    # =====================================================================
    # FUNCIONES DE INTERACCIÓN Y PROCESOS DE DATOS
    # =====================================================================

    def actualizar_tablas(self):
        """Limpia los listados e inserta los datos actualizados del sistema."""
        for item in self.tree_avl.get_children():
            self.tree_avl.delete(item)
        for item in self.tree_heap.get_children():
            self.tree_heap.delete(item)

        # Rellenar tabla AVL (Ordenada recursivamente)
        tareas_avl = self.sistema.listar_tareas_por_id()
        for t in tareas_avl:
            self.tree_avl.insert('', tk.END, values=(t.id, t.nombre, t.prioridad))

        # Rellenar tabla Heap (Por nivel de urgencia)
        tareas_heap = self.sistema.listar_tareas_por_prioridad()
        for t in tareas_heap:
            self.tree_heap.insert('', tk.END, values=(t.id, t.nombre, t.prioridad))

        # Actualización de contador
        self.lbl_contador.config(text=f"Tareas activas en memoria: {self.sistema.cantidad_tareas()}")

    def al_seleccionar_tarea(self, event):
        """Escribe automáticamente el ID de la fila clicada en las cajas de texto."""
        tree = event.widget
        seleccion = tree.selection()
        if seleccion:
            item_data = tree.item(seleccion[0], 'values')
            self.ent_id_accion.delete(0, tk.END)
            self.ent_id_accion.insert(0, item_data[0])

    def agregar_tarea(self):
        try:
            id_tarea = int(self.ent_id.get().strip())
            nombre = self.ent_nombre.get().strip()
            prioridad = int(self.ent_prioridad.get().strip())
        except ValueError:
            messagebox.showerror("Campos Inválidos", "Tanto el 'ID' como la 'Prioridad' deben contener caracteres numéricos enteros.")
            return

        if not nombre:
            messagebox.showerror("Campo Vacío", "Por favor, define una descripción para la tarea.")
            return

        exito = self.sistema.agregar_tarea(id_tarea, nombre, prioridad)
        if exito:
            messagebox.showinfo("Proceso Completo", f"Tarea registrada exitosamente:\n'{nombre}'")
            self.ent_id.delete(0, tk.END)
            self.ent_nombre.delete(0, tk.END)
            self.ent_prioridad.delete(0, tk.END)
            self.actualizar_tablas()
        else:
            messagebox.showerror("ID Duplicado", f"El ID {id_tarea} ya pertenece a otra tarea activa.")

    def atender_tarea(self):
        tarea = self.sistema.atender_tarea()
        if tarea:
            messagebox.showinfo(
                "Despachando Tarea", 
                f"Siguiente tarea prioritaria en ejecución:\n\n"
                f"• ID: {tarea.id}\n"
                f"• Nombre: {tarea.nombre}\n"
                f"• Prioridad asignada: {tarea.prioridad}"
            )
            self.actualizar_tablas()
        else:
            messagebox.showwarning("Cola Vacía", "No existen tareas actualmente programadas en el sistema.")

    def buscar_tarea(self):
        try:
            id_tarea = int(self.ent_id_accion.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Inserta un número ID válido en el Panel de Control.")
            return

        tarea = self.sistema.buscar_tarea(id_tarea)
        if tarea:
            messagebox.showinfo(
                "Búsqueda Exitosa", 
                f"Información de la Tarea Encontrada:\n\n"
                f"• ID: {tarea.id}\n"
                f"• Descripción: {tarea.nombre}\n"
                f"• Prioridad actual: {tarea.prioridad}"
            )
        else:
            messagebox.showerror("Sin Coincidencias", f"No se encontró la tarea con el ID: {id_tarea}.")

    def eliminar_tarea(self):
        try:
            id_tarea = int(self.ent_id_accion.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Inserta un número ID válido en el Panel de Control.")
            return

        tarea = self.sistema.completar_tarea(id_tarea)
        if tarea:
            messagebox.showinfo("Tarea Removida", f"La tarea con ID {id_tarea} ha sido removida del sistema.")
            self.ent_id_accion.delete(0, tk.END)
            self.actualizar_tablas()
        else:
            messagebox.showerror("Fallo de Eliminación", f"No existe la tarea con el ID: {id_tarea}.")

    def modificar_prioridad(self):
        try:
            id_tarea = int(self.ent_id_accion.get().strip())
            nueva_prioridad = int(self.ent_nueva_prioridad.get().strip())
        except ValueError:
            messagebox.showerror("Campos Vacíos/Erróneos", "Es indispensable especificar el ID de la tarea y la nueva prioridad (ambos numéricos).")
            return

        exito = self.sistema.modificar_prioridad(id_tarea, nueva_prioridad)
        if exito:
            messagebox.showinfo("Prioridad Modificada", f"La prioridad de la tarea {id_tarea} cambió exitosamente a {nueva_prioridad}.")
            self.ent_nueva_prioridad.delete(0, tk.END)
            self.actualizar_tablas()
        else:
            messagebox.showerror("Error", f"No fue posible encontrar la tarea con el ID {id_tarea} en el Árbol AVL.")


# =====================================================================
# 4. DISPARADOR PRINCIPAL
# =====================================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = SistemaTareasGUI(root)
    root.mainloop()
