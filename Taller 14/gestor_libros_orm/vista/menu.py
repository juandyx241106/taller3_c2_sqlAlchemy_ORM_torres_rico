"""
Módulo: vista.menu
Proporciona una interfaz de texto para interactuar con el controlador.
"""

from gestor_libros_orm.controlador import operaciones


def mostrar_menu():
    while True:
        print("\n--- GESTOR DE LIBROS (ORM) ---")
        print("1. Agregar libro")
        print("2. Listar todos")
        print("3. Buscar por categoría")
        print("4. Actualizar precio por título")
        print("5. Eliminar por título")
        print("6. Inserción concurrente")
        print("7. Salir")

        op = input("Seleccione una opción: ")

        if op == "1":
            t = input("Título: ")
            a = input("Autor: ")
            p = float(input("Precio: "))
            y = int(input("Año: "))
            c = input("Categoría: ")
            operaciones.agregar_libro(t, a, p, y, c)

        elif op == "2":
            operaciones.listar_libros()

        elif op == "3":
            c = input("Categoría: ")
            operaciones.buscar_por_categoria(c)

        elif op == "4":
            t = input("Título del libro: ")
            np = float(input("Nuevo precio: "))
            operaciones.actualizar_precio(t, np)

        elif op == "5":
            t = input("Título del libro a eliminar: ")
            operaciones.eliminar_libro(t)

        elif op == "6":
            operaciones.insertar_concurrencia()

        elif op == "7":
            print("Fin de la sesión.")
            break
        else:
            print("Opción no válida.")
