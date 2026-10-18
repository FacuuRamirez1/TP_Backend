# Trabajo Práctico - Librería

API asincrónica de catálogo, clientes y ventas para Programación III (UTN),
implementada con FastAPI, SQLModel, SQLAlchemy async, PostgreSQL y Alembic.

Las tablas se crean exclusivamente mediante las migraciones de Alembic. El
archivo `.env` contiene la configuración local y no debe versionarse; para
configurarlo se utiliza [env.example](./env.example).

## Requisitos previos

- Python 3.12 instalado y disponible como `py -3.12`.
- PostgreSQL 16 instalado y ejecutándose.
- Una base de datos PostgreSQL vacía llamada `libreria`.
- PowerShell en Windows.

## 1. Crear el entorno virtual

Abrir PowerShell en la raíz del proyecto:

```powershell
cd "C:\ruta\al\proyecto\Relaciones Libreria"
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si PowerShell impide activar scripts por la política de ejecución, ejecutar
`Set-ExecutionPolicy -Scope Process Bypass` en esa misma consola y volver a
activar el entorno.

## 2. Instalar dependencias

Con `.venv` activo, actualizar `pip` e instalar las dependencias:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

El archivo [requirements.txt](./requirements.txt) incluye:

- `pydantic[email]`, necesario para validar emails mediante `EmailStr`.
- `greenlet`, requerido por SQLAlchemy para su soporte asincrónico.
- FastAPI, SQLModel, SQLAlchemy, asyncpg, Alembic, python-dotenv y Uvicorn.

Estas dependencias se instalan normalmente como wheels precompilados en
Python 3.12. Si se usa otro intérprete, se recomienda volver a crear el
entorno con Python 3.12 antes de instalar.

## 3. Configurar `.env`

Copiar el archivo de ejemplo:

```powershell
Copy-Item env.example .env
```

Editar `.env` y reemplazar `usuario` y `pass` por las credenciales locales de
PostgreSQL:

```dotenv
DATABASE_URL=postgresql+asyncpg://usuario:pass@localhost:5432/libreria
ECHO_SQL=false
```

Para observar las consultas SQL del caso C-07, cambiar temporalmente
`ECHO_SQL=true`. El archivo `.env` no debe subirse al repositorio.

## 4. Aplicar las migraciones

Con PostgreSQL ejecutándose, aplicar todas las migraciones:

```powershell
alembic upgrade head
```

La carpeta [migrations/](./migrations/) contiene la configuración asincrónica de
Alembic y dos revisiones generadas con `--autogenerate`:

1. `6febc85e97a1`: crea las tablas del catálogo, clientes y ventas, excepto
   `genero`.
2. `036ddd331c89`: crea `genero` y agrega `libro.genero_id`.

La segunda revisión se corrigió a mano después de leerla: `--autogenerate` emitió
la foreign key de `libro.genero_id` sin nombre (`create_foreign_key(None, ...)`),
lo que hacía fallar el `downgrade`. Se le asignó el nombre
`fk_libro_genero_id_genero` (ver el comentario en el propio archivo). Además se
agregó `import sqlmodel` al template `script.py.mako`, que faltaba para las
columnas generadas por SQLModel.

Para comprobar el ciclo de downgrade y upgrade:

```powershell
alembic downgrade -1
alembic upgrade head
```

## 5. Cargar datos iniciales

Después de aplicar las migraciones, ejecutar:

```powershell
python -m scripts.seed
```

El script carga un conjunto reproducible con editorial, género, dos autores,
cuatro libros, cliente, perfil y autorías con rol y orden. Incluye los libros
utilizados por el caso C-06. No sobrescribe una base que ya contiene
editoriales.

## 6. Arrancar el servidor

```powershell
uvicorn app.main:app --reload
```

La API queda disponible en:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Health live: <http://localhost:8000/health/live>
- Health ready: <http://localhost:8000/health/ready>

## Pruebas C-01 a C-08

La carpeta [test/](./test/) contiene los archivos `.http` solicitados:

- `C-01-validacion-ruta.http`: parámetro de ruta no entero.
- `C-02-unicidad.http`: ISBN y email repetidos.
- `C-03-perfil-unico.http`: segundo perfil del mismo cliente.
- `C-04-fk-libro.http`: editorial o autor inexistente.
- `C-05-venta-invalida.http`: cliente o libro inexistente.
- `C-06-venta-valida.http`: venta con dos renglones, precios copiados y total calculado.
- `C-07-detalles.http`: detalles de libro y venta sin N+1.
- `C-08-busqueda-segura.http`: búsqueda por título con texto similar a SQL.

Los archivos son compatibles con la extensión REST Client de VS Code. El caso
C-07 puede verificarse con las consultas en consola activando `ECHO_SQL=true`
antes de arrancar Uvicorn.

Antes de correr `C-06` y `C-07` hay que ejecutar `python -m scripts.seed`; `C-07`
consulta `GET /ventas/1`, que crea el caso `C-06`.

## Evidencia del caso C-07


### 1. Detalle de un libro (`GET /libros/1`)

![Detalle de libro con el SQL en consola](./capturas_C-07/C-07-libros.png)


### 2. Detalle de una venta (`GET /ventas/1`)

![Detalle de venta con el SQL en consola](./capturas_C-07/C-07-ventas.png)
