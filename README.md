# FastAPI Demo

Backend REST API desarrollado con **FastAPI**, **SQLModel**, **MySQL** y **Alembic**.

El proyecto tiene como objetivo servir como aplicación de ejemplo para aprender y practicar desarrollo de APIs con Python, incluyendo persistencia de datos, relaciones entre entidades, migraciones, validación de datos y separación de responsabilidades.

## 🛠️ Stack tecnológico

* **Python 3.12+**
* **FastAPI**
* **SQLModel**
* **SQLAlchemy**
* **MySQL**
* **Alembic**
* **Uvicorn**
* **uv** — gestión de dependencias y entorno virtual

## 🏗️ Arquitectura

El proyecto utiliza una **arquitectura por capas (Layered Architecture)** organizada por funcionalidades.

```text
app/
├── core/
│   ├── config.py
│   ├── database.py
│   └── security.py
│
├── users/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
│
├── projects/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
│
├── tasks/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
│
├── comments/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
│
├── tags/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── router.py
│
├── models.py
└── main.py
│
├── alembic/
│   ├── versions/
│   └── env.py
│
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .env
├── .env.example
├── .gitignore
└── README.md
```

### Flujo de una petición

```text
HTTP Request
     │
     ▼
┌─────────────┐
│    Router   │
│ Controller  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │
│   Business  │
│    Logic    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ Repository  │
│ Data Access │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   SQLModel  │
└──────┬──────┘
       │
       ▼
     MySQL
```

# 🚀 Instalación

## Requisitos

Necesitas tener instalado:

* Python 3.12+
* MySQL 8+
* uv

Comprueba las versiones:

```bash
python --version
mysql --version
uv --version
```

## Clonar el proyecto

```bash
git clone <repository-url>
cd fast-api-tutorial
```

## Instalar dependencias

```bash
uv sync
```

Esto instalará las dependencias definidas en `pyproject.toml`.

---

# ⚙️ Configuración

Crea un archivo `.env` en la raíz del proyecto:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fastapi_demo
```

No debes subir el archivo `.env` al repositorio.

Puedes utilizar `.env.example` como plantilla:

```env
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/fastapi_demo
```

---

# 🗄️ Base de datos

Crea la base de datos en MySQL:

```sql
CREATE DATABASE fastapi_demo
CHARACTER SET utf8mb4
COLLATE utf8mb4_general_ci;
```

La estructura de la base de datos se gestiona mediante **Alembic**.

---

# 🔄 Migraciones con Alembic

Para comprobar la migración actual:

```bash
uv run alembic current
```

Ver el historial:

```bash
uv run alembic history
```

Crear una nueva migración automáticamente:

```bash
uv run alembic revision --autogenerate -m "description of changes"
```

Aplicar las migraciones:

```bash
uv run alembic upgrade head
```

Retroceder una migración:

```bash
uv run alembic downgrade -1
```

# ▶️ Ejecutar la aplicación

Puedes iniciar el servidor con:

```bash
uv run fastapi dev
```

La API estará disponible normalmente en:

```text
http://localhost:8000
```

## Documentación

FastAPI genera automáticamente documentación OpenAPI.

Swagger UI:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# 🧪 Probar la API

Por ejemplo:

```bash
curl http://localhost:8000/users/
```

También puedes utilizar Swagger:

```text
http://localhost:8000/docs
```

para ejecutar los endpoints directamente desde el navegador.

---

# 🧩 Responsabilidades de cada capa

## Router

Se encarga de las responsabilidades HTTP:

* endpoints
* parámetros
* status codes
* dependencias
* request/response

Ejemplo:

```python
@router.get("/", response_model=list[UserRead])
def get_users(session: Session = Depends(get_session)):
    return list_users(session)
```

## Service

Contiene la lógica de negocio.

```text
Router
   ↓
Service
```

El service no debería preocuparse por detalles de HTTP.

## Repository

Se encarga del acceso a datos.

```text
Service
   ↓
Repository
   ↓
Database
```

## Schemas

Representan los contratos de la API.

Por ejemplo:

```text
UserCreate
UserUpdate
UserRead
```

Evitan exponer directamente información interna del modelo de persistencia.

## Models

Representan las entidades persistentes y sus relaciones.

Son utilizados por SQLModel/SQLAlchemy para mapear objetos Python con tablas de MySQL.

---

# 🔐 Seguridad

La configuración relacionada con seguridad se encuentra en:

```text
app/core/security.py
```

# 📄 License

This project is intended for educational and demonstration purposes.

