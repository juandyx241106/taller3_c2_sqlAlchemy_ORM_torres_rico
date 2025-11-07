"""
Módulo: controlador.operaciones
Contiene las funciones CRUD, transacciones y concurrencia.
"""

from threading import Lock, Thread
from sqlalchemy.exc import SQLAlchemyError
from gestor_libros_orm.modelo.libro import SessionLocal, Libro, Categoria

lock = Lock()


def agregar_libro(titulo, autor, precio, año, categoria_nombre):
    """Agrega un libro con manejo de transacciones y bloqueo concurrente."""
    session = SessionLocal()
    try:
        with lock:
            categoria = (
                session.query(Categoria).filter_by(nombre=categoria_nombre).first()
            )
            if not categoria:
                categoria = Categoria(nombre=categoria_nombre)
                session.add(categoria)
                session.commit()

            nuevo = Libro(
                titulo=titulo, autor=autor, precio=precio, año=año, categoria=categoria
            )
            session.add(nuevo)
            session.commit()
            print("Libro agregado correctamente.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error al agregar libro:", e)
    finally:
        session.close()


def listar_libros():
    """Lista todos los libros registrados."""
    session = SessionLocal()
    libros = session.query(Libro).all()
    if libros:
        print(
            f"{'ID':<5}{'Título':<25}{'Autor':<20}{'Precio':<10}{'Año':<6}{'Categoría':<15}"
        )
        for libro in libros:
            print(
                f"{libro.id:<5}{libro.titulo[:22]:<25}{libro.autor[:18]:<20}{libro.precio:<10}{libro.año:<6}{libro.categoria.nombre[:13] if libro.categoria else 'N/A':<15}"
            )

    else:
        print("No hay registros.")
    session.close()


def buscar_por_categoria(nombre_categoria):
    """Muestra libros filtrados por categoría."""
    session = SessionLocal()
    categoria = session.query(Categoria).filter_by(nombre=nombre_categoria).first()
    if not categoria:
        print("Categoría no encontrada.")
    else:
        print(f"\nLibros en la categoría '{nombre_categoria}':")
        for libro in categoria.libros:
            print(f"- {libro.titulo} ({libro.autor}) - ${libro.precio}")
    session.close()


def actualizar_precio(titulo, nuevo_precio):
    """Actualiza el precio de un libro según su título."""
    session = SessionLocal()
    try:
        libro = session.query(Libro).filter_by(titulo=titulo).first()
        if libro:
            libro.precio = nuevo_precio
            session.commit()
            print("Precio actualizado correctamente.")
        else:
            print("Libro no encontrado.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()


def eliminar_libro(titulo):
    """Elimina un libro por título."""
    session = SessionLocal()
    try:
        libro = session.query(Libro).filter_by(titulo=titulo).first()
        if libro:
            session.delete(libro)
            session.commit()
            print("Libro eliminado.")
        else:
            print("Libro no encontrado.")
    except SQLAlchemyError as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()


def insertar_concurrencia():
    """Simula concurrencia: tres hilos insertando libros."""

    def tarea(i):
        agregar_libro(f"Libro{i}", "AutorX", 5000 + i * 1000, 2020 + i, "Concurrencia")

    hilos = [Thread(target=tarea, args=(i,)) for i in range(1, 4)]
    for h in hilos:
        h.start()
    for h in hilos:
        h.join()
    print("Inserción concurrente finalizada.")
