"""
Módulo: modelo.libro
Define las clases ORM 'Categoria' y 'Libro' y configura la conexión a la base de datos.
"""

from pathlib import Path
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from typing import Any

Base: Any = declarative_base()

DATA_DIR = Path("datos")
DATA_DIR.mkdir(exist_ok=True)
DB_URL = f"sqlite:///{(DATA_DIR / 'libros.db').as_posix()}"

engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


class Categoria(Base):
    """Clase ORM que representa una categoría de libros."""

    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String, nullable=False, unique=True)

    libros = relationship(
        "Libro", back_populates="categoria", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Categoria(id={self.id}, nombre='{self.nombre}')>"


class Libro(Base):  # type: ignore[valid-type]
    """Clase ORM que representa un libro en la base de datos."""

    __tablename__ = "libros"

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    autor = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    año = Column(Integer, nullable=False)
    categoria_id = Column(Integer, ForeignKey("categorias.id"), nullable=False)

    categoria = relationship("Categoria", back_populates="libros")

    def __repr__(self):
        return (
            f"<Libro(id={self.id}, titulo='{self.titulo}', autor='{self.autor}', "
            f"precio={self.precio}, año={self.año}, categoria_id={self.categoria_id})>"
        )


Base.metadata.create_all(engine)
