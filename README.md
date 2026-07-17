#  Sistema de Gestión de Tareas — MaxHeap + Árbol AVL

> Proyecto académico para el curso de **Análisis de Algoritmos** — Universidad del Valle  
> Implementación de una cola de prioridad híbrida usando **MaxHeap** y **Árbol AVL** en Python puro.

---

##  Descripción

Este sistema permite gestionar tareas con distintos niveles de prioridad combinando dos estructuras de datos complementarias:

| Estructura | Rol en el sistema |
|---|---|
| **MaxHeap** | Cola de prioridad — extrae siempre la tarea más urgente en O(log n) |
| **Árbol AVL** | Índice por ID — búsqueda, inserción y eliminación balanceada en O(log n) |

Ambas estructuras permanecen **sincronizadas en todo momento**: cualquier inserción, eliminación o actualización de prioridad se propaga automáticamente a las dos.

---

## 🗂️ Estructura del Proyecto

```
Proyecto_Heap_AVL/
│
├── main.py            ← Punto de entrada — menú interactivo en consola
├── tarea.py           ← Clase Tarea (modelo de datos)
├── heap.py            ← Clase MaxHeap (cola de prioridad)
├── avl.py             ← Clases NodoAVL y AVL (árbol de búsqueda balanceado)
├── sistema_tareas.py  ← Clase integradora SistemaTareas (Heap + AVL)
├── notebook.ipynb     ← Desarrollo paso a paso y explicación didáctica
└── README.md          ← Este archivo
```

---

## 📄 Descripción de cada archivo

### `tarea.py`
Define la clase `Tarea`, unidad básica del sistema.

```python
Tarea(id, nombre, prioridad)
```

| Atributo | Tipo | Descripción |
|---|---|---|
| `id` | `int` | Identificador único de la tarea |
| `nombre` | `str` | Descripción de la tarea |
| `prioridad` | `int` | Nivel de urgencia (mayor = más prioritario) |

---

### `heap.py`
Implementa la clase `MaxHeap`: cola de prioridad basada en un arreglo.

| Método | Complejidad | Descripción |
|---|---|---|
| `insertar(tarea)` | O(log n) | Agrega una tarea y sube al lugar correcto |
| `extraer_maximo()` | O(log n) | Elimina y retorna la tarea de mayor prioridad |
| `ver_maximo()` | O(1) | Consulta la tarea más prioritaria sin eliminarla |
| `eliminar_por_id(id)` | O(n) + O(log n) | Elimina cualquier tarea por su ID |
| `actualizar_prioridad(id, nueva)` | O(n) + O(log n) | Cambia la prioridad y reordena el heap |
| `esta_vacio()` | O(1) | Indica si el heap está vacío |
| `tamano()` | O(1) | Cantidad de elementos en el heap |

---

### `avl.py`
Implementa las clases `NodoAVL` y `AVL`: árbol binario de búsqueda auto-balanceado, indexado por el **ID** de cada tarea.

| Método | Complejidad | Descripción |
|---|---|---|
| `insertar(tarea)` | O(log n) | Inserta y aplica rotaciones LL, RR, LR o RL si es necesario |
| `buscar(id)` | O(log n) | Retorna la tarea con ese ID o `None` |
| `eliminar(id)` | O(log n) | Elimina el nodo y rebalancea en cascada |
| `inorden()` | O(n) | Retorna la lista de tareas ordenadas por ID ascendente |

Los cuatro casos de rotación garantizan que el árbol nunca supere una diferencia de altura de 1 entre subárboles.

---

### `sistema_tareas.py`
Clase `SistemaTareas`: coordina e integra el `MaxHeap` y el `AVL`, manteniendo ambas estructuras consistentes.

| Método | Descripción |
|---|---|
| `agregar_tarea(id, nombre, prioridad)` | Inserta la tarea en heap y AVL; rechaza IDs duplicados |
| `buscar_tarea(id)` | Búsqueda rápida por ID vía AVL |
| `atender_tarea()` | Extrae la tarea más prioritaria del heap y la elimina del AVL |
| `completar_tarea(id)` | Marca una tarea como completada eliminándola de ambas estructuras |
| `eliminar_tarea(id)` | Elimina una tarea por ID de ambas estructuras |
| `modificar_prioridad(id, nueva)` | Actualiza la prioridad en heap y AVL simultáneamente |
| `listar_tareas_por_id()` | Lista todas las tareas ordenadas por ID (recorrido inorden del AVL) |
| `listar_tareas_por_prioridad()` | Lista todas las tareas de mayor a menor prioridad |
| `cantidad_tareas()` | Retorna el número total de tareas activas |

---

### `main.py`
Interfaz interactiva en consola con colores ANSI, tablas formateadas y validación de entradas.

**Opciones del menú:**

```
1. Agregar nueva tarea
2. Atender tarea de mayor prioridad
3. Completar tarea por ID
4. Buscar tarea por ID
5. Eliminar tarea por ID
6. Modificar prioridad de una tarea
7. Listar tareas ordenadas por ID     (AVL inorden)
8. Listar tareas ordenadas por Prioridad (MaxHeap)
9. Salir
```

---

### `notebook.ipynb`
Cuaderno Jupyter con el desarrollo incremental del proyecto: construcción célula a célula del `MaxHeap` y el `AVL`, con ejemplos de ejecución y salidas documentadas.

---

## 🚀 Cómo ejecutar el proyecto

### Requisitos

- **Python 3.8 o superior**
- No se requieren librerías externas — sólo biblioteca estándar de Python

Verificá tu versión con:
```bash
python3 --version
```

---

### Opción 1 — Ejecutar directamente (recomendado)

Desde la raíz del repositorio, entrar a la carpeta del proyecto:

```bash
cd Proyecto_Heap_AVL
python3 main.py
```

---

### Opción 2 — Clonar el repositorio y ejecutar

```bash
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>/Proyecto_Heap_AVL
python3 main.py
```

---

### Opción 3 — Explorar el notebook

Si tenés Jupyter instalado:

```bash
pip install notebook
jupyter notebook notebook.ipynb
```

O podés abrirlo directamente en **VS Code** con la extensión de Jupyter.

---

##  Complejidad de las Operaciones Principales

| Operación | MaxHeap | AVL | Sistema (combinado) |
|---|---|---|---|
| Agregar tarea | O(log n) | O(log n) | O(log n) |
| Atender (extraer máximo) | O(log n) | O(log n) | O(log n) |
| Buscar por ID | O(n) | **O(log n)** | O(log n) |
| Eliminar/Completar por ID | O(n) + O(log n) | O(log n) | O(n) |
| Modificar prioridad | O(n) + O(log n) | O(log n) | O(n) |
| Listar por ID (inorden) | — | O(n) | O(n) |
| Listar por prioridad | — | O(n log n) | O(n log n) |

---

## 🏗️ Decisiones de Diseño

- **¿Por qué dos estructuras?** El MaxHeap es óptimo para extraer el máximo pero no permite búsqueda eficiente por ID. El AVL complementa esa carencia con búsqueda y eliminación en O(log n).
- **Consistencia garantizada:** Toda operación en `SistemaTareas` actualiza ambas estructuras atómicamente, evitando estados inconsistentes.
- **Sin dependencias externas:** El proyecto usa únicamente Python estándar, lo que facilita su ejecución en cualquier entorno académico.

---

## 👨‍💻 Autores

**Juan David Solarte**  
**Maria Baracaldo**  
Ingeniería de Sistemas — Universidad del Valle  
Curso: Análisis de Algoritmos
