import sys

# Colores ANSI para mejorar la interfaz en consola
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
MAGENTA = "\033[95m"
CYAN = "\033[96m"

try:
    from .sistema_tareas import SistemaTareas
except ImportError:
    try:
        from sistema_tareas import SistemaTareas
    except ImportError:
        # Agregar el directorio actual al path en caso de ejecución directa desde otros directorios
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        from sistema_tareas import SistemaTareas

def mostrar_banner():
    banner = f"""{BOLD}{CYAN}
  ██████╗ ██████╗  ██████╗ ██╗   ██╗███████╗ ██████╗████████╗ ██████╗ 
  ██╔══██╗██╔══██╗██╔═══██╗╚██╗ ██╔╝██╔════╝██╔════╝╚══██╔══╝██╔═══██╗
  ██████╔╝██████╔╝██║   ██║ ╚████╔╝ █████╗  ██║        ██║   ██║   ██║
  ██╔═══╝ ██╔══██╗██║   ██║  ╚██╔╝  ██╔══╝  ██║        ██║   ██║   ██║
  ██║     ██║  ██║╚██████╔╝   ██║   ███████╗╚██████╗   ██║   ╚██████╔╝
  ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚══════╝ ╚═════╝   ╚═╝    ╚═════╝ 
        {RESET}{BOLD}{YELLOW}S I S T E M A   D E   G E S T I O N   D E   T A R E A S{RESET}
                     {MAGENTA}(MaxHeap + Árbol AVL){RESET}
    """
    print(banner)

def leer_entero(mensaje, valor_minimo=None):
    """
    Lee un número entero de consola y valida la entrada.
    """
    while True:
        try:
            entrada = input(mensaje).strip()
            if not entrada:
                print(f"{RED}Error: La entrada no puede estar vacía.{RESET}")
                continue
            valor = int(entrada)
            if valor_minimo is not None and valor < valor_minimo:
                print(f"{RED}Error: El valor debe ser mayor o igual a {valor_minimo}.{RESET}")
                continue
            return valor
        except ValueError:
            print(f"{RED}Error: Ingrese un número entero válido.{RESET}")

def leer_texto(mensaje):
    """
    Lee una cadena de texto y asegura que no esté vacía.
    """
    while True:
        entrada = input(mensaje).strip()
        if not entrada:
            print(f"{RED}Error: El texto no puede estar vacío.{RESET}")
            continue
        return entrada

def imprimir_tabla(tareas, titulo):
    """
    Dibuja una tabla de tareas formateada en consola.
    """
    print(f"\n{BOLD}{CYAN}=== {titulo} ==={RESET}")
    if not tareas:
        print(f"{YELLOW}No hay tareas en el sistema.{RESET}")
        return

    # Encabezados
    col_id = 8
    col_nombre = 28
    col_prioridad = 10

    linea_divisoria = f"+{'-' * (col_id + 2)}+{'-' * (col_nombre + 2)}+{'-' * (col_prioridad + 2)}+"
    print(linea_divisoria)
    print(f"| {'ID':<{col_id}} | {'Nombre':<{col_nombre}} | {'Prioridad':<{col_prioridad}} |")
    print(linea_divisoria)

    for t in tareas:
        # Truncar nombre si es muy largo para la tabla
        nombre_truncado = t.nombre[:col_nombre-3] + "..." if len(t.nombre) > col_nombre else t.nombre
        print(f"| {t.id:<{col_id}} | {nombre_truncado:<{col_nombre}} | {t.prioridad:<{col_prioridad}} |")
    
    print(linea_divisoria)
    print(f"{BOLD}Total: {len(tareas)} tarea(s){RESET}\n")

def menu_principal():
    sistema = SistemaTareas()
    
    # Insertar algunas tareas de prueba iniciales
    sistema.agregar_tarea(101, "Configurar base de datos", 8)
    sistema.agregar_tarea(102, "Diseñar interfaz de usuario", 5)
    sistema.agregar_tarea(103, "Pruebas de seguridad", 10)
    sistema.agregar_tarea(104, "Redactar documentación", 3)

    while True:
        mostrar_banner()
        print(f"{BOLD}{BLUE}--- MENU PRINCIPAL ---{RESET}")
        print(f"{GREEN}1.{RESET} Agregar nueva tarea")
        print(f"{GREEN}2.{RESET} Atender tarea de mayor prioridad")
        print(f"{GREEN}3.{RESET} Buscar tarea por ID")
        print(f"{GREEN}4.{RESET} Eliminar tarea por ID")
        print(f"{GREEN}5.{RESET} Modificar prioridad de una tarea")
        print(f"{GREEN}6.{RESET} Listar tareas ordenadas por ID (AVL Tree)")
        print(f"{GREEN}7.{RESET} Listar tareas ordenadas por Prioridad (MaxHeap)")
        print(f"{GREEN}8.{RESET} Salir")
        print("-" * 30)

        opcion = leer_entero(f"{BOLD}Seleccione una opción (1-8): {RESET}", 1)

        if opcion == 1:
            print(f"\n{BOLD}{BLUE}[Agregar Nueva Tarea]{RESET}")
            id_tarea = leer_entero("Ingrese el ID único de la tarea (positivo): ", 1)
            nombre = leer_texto("Ingrese el nombre/descripción de la tarea: ")
            prioridad = leer_entero("Ingrese el nivel de prioridad (entero >= 0): ", 0)

            exito = sistema.agregar_tarea(id_tarea, nombre, prioridad)
            if exito:
                print(f"\n{GREEN}✔ Tarea agregada correctamente.{RESET}")
            else:
                print(f"\n{RED}❌ Error: El ID {id_tarea} ya existe en el sistema.{RESET}")

        elif opcion == 2:
            print(f"\n{BOLD}{BLUE}[Atender Tarea Prioritaria]{RESET}")
            tarea = sistema.atender_tarea()
            if tarea:
                print(f"\n{GREEN}✔ Atendiendo tarea de mayor prioridad:{RESET}")
                print(f"  {BOLD}ID:{RESET} {tarea.id}")
                print(f"  {BOLD}Nombre:{RESET} {tarea.nombre}")
                print(f"  {BOLD}Prioridad:{RESET} {tarea.prioridad}")
            else:
                print(f"\n{YELLOW}No hay tareas pendientes en el sistema.{RESET}")

        elif opcion == 3:
            print(f"\n{BOLD}{BLUE}[Buscar Tarea por ID]{RESET}")
            id_tarea = leer_entero("Ingrese el ID de la tarea a buscar: ", 1)
            tarea = sistema.buscar_tarea(id_tarea)
            if tarea:
                print(f"\n{GREEN}✔ Tarea encontrada:{RESET}")
                print(f"  {BOLD}ID:{RESET} {tarea.id}")
                print(f"  {BOLD}Nombre:{RESET} {tarea.nombre}")
                print(f"  {BOLD}Prioridad:{RESET} {tarea.prioridad}")
            else:
                print(f"\n{RED}❌ Tarea con ID {id_tarea} no encontrada.{RESET}")

        elif opcion == 4:
            print(f"\n{BOLD}{BLUE}[Eliminar Tarea por ID]{RESET}")
            id_tarea = leer_entero("Ingrese el ID de la tarea a eliminar: ", 1)
            tarea = sistema.eliminar_tarea(id_tarea)
            if tarea:
                print(f"\n{GREEN}✔ Tarea eliminada correctamente:{RESET}")
                print(f"  {tarea}{RESET}")
            else:
                print(f"\n{RED}❌ No se encontró ninguna tarea con ID {id_tarea}.{RESET}")

        elif opcion == 5:
            print(f"\n{BOLD}{BLUE}[Modificar Prioridad]{RESET}")
            id_tarea = leer_entero("Ingrese el ID de la tarea a modificar: ", 1)
            tarea = sistema.buscar_tarea(id_tarea)
            if tarea:
                print(f"Tarea actual: {tarea}")
                nueva_prioridad = leer_entero("Ingrese la nueva prioridad (entero >= 0): ", 0)
                sistema.modificar_prioridad(id_tarea, nueva_prioridad)
                print(f"\n{GREEN}✔ Prioridad actualizada correctamente.{RESET}")
            else:
                print(f"\n{RED}❌ Tarea con ID {id_tarea} no encontrada.{RESET}")

        elif opcion == 6:
            tareas = sistema.listar_tareas_por_id()
            imprimir_tabla(tareas, "TAREAS ORDENADAS POR ID (AVL INORDEN)")

        elif opcion == 7:
            tareas = sistema.listar_tareas_por_prioridad()
            imprimir_tabla(tareas, "TAREAS ORDENADAS POR PRIORIDAD (MAXHEAP ORDENADO)")

        elif opcion == 8:
            print(f"\n{BOLD}{YELLOW}¡Gracias por usar el sistema! Saliendo...{RESET}\n")
            break

        else:
            print(f"{RED}Opción no válida. Intente de nuevo.{RESET}")

        input(f"\nPresione {BOLD}Enter{RESET} para continuar...")

if __name__ == "__main__":
    menu_principal()
