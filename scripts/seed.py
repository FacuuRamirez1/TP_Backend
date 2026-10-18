import asyncio

from sqlalchemy import select

from app.core.database import create_database_resources
from app.modules.autores.models import Autor
from app.modules.clientes.models import Cliente
from app.modules.editoriales.models import Editorial
from app.modules.generos.models import Genero
from app.modules.libros.models import Libro, LibroAutor
from app.modules.clientes.models import PerfilCliente
from decimal import Decimal


async def seed() -> None:
    engine, session_maker = create_database_resources()
    async with session_maker() as session:
        if (await session.execute(select(Editorial).limit(1))).scalar_one_or_none() is not None:
            print("La base ya contiene datos; no se modificó.")
            await engine.dispose()
            return
        editorial = Editorial(nombre="Editorial de prueba", pais="Argentina")
        genero = Genero(nombre="Narrativa")
        autor = Autor(nombre="Autor de prueba", nacionalidad="Argentina")
        coautor = Autor(nombre="Coautor de prueba", nacionalidad="Argentina")
        cliente = Cliente(nombre="Tomás Ríos", email="tomas@example.com")
        session.add_all([editorial, genero, autor, coautor, cliente])
        await session.commit()
        books = [
            Libro(isbn="978-950-00-0001-1", titulo="Rayuela", precio=Decimal("25000.00"), stock=10, editorial_id=editorial.id, genero_id=genero.id),
            Libro(isbn="978-950-00-0002-8", titulo="El túnel", precio=Decimal("18000.00"), stock=10, editorial_id=editorial.id, genero_id=genero.id),
            Libro(isbn="978-950-00-0003-5", titulo="Sobre héroes y tumbas", precio=Decimal("22000.00"), stock=10, editorial_id=editorial.id, genero_id=genero.id),
            Libro(isbn="978-950-00-0004-2", titulo="Respiración artificial", precio=Decimal("27000.00"), stock=10, editorial_id=editorial.id, genero_id=genero.id),
        ]
        session.add_all(books)
        await session.flush()
        books[0].autorias.append(LibroAutor(autor_id=autor.id, rol="autor", orden=1))
        books[3].autorias.extend([
            LibroAutor(autor_id=autor.id, rol="autor", orden=1),
            LibroAutor(autor_id=coautor.id, rol="coautor", orden=2),
        ])
        session.add(PerfilCliente(cliente_id=cliente.id, telefono="11-5555-0000", direccion="Calle de prueba 123"))
        await session.commit()
        print("Datos iniciales cargados: editoriales, género, autores, libros 1-4, cliente y perfil.")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed())
