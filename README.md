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

## 📦 Entidades

La aplicación utiliza las siguientes entidades:

```text
User
 │
 ├── Project
 │      │
 │      └── Task
 │            │
 │            ├── TaskComment
 │            │       └── User
 │            │
 │            └── TaskTag
 │                   └── Tag
```

### User

Representa los usuarios de la aplicación.

Principales campos:

* `id`
* `name`
* `email`
* `password_hash`
* `is_active`
* `created_at`
* `updated_at`

### Project

Representa proyectos pertenecientes a usuarios.

Relación:

```text
User 1 ─────── N Project
```

### Task

Representa tareas asociadas a un proyecto.

Relaciones:

```text
Project 1 ─────── N Task

User 1 ────────── N Task
```

Un usuario puede tener múltiples tareas asignadas.

### TaskComment

Representa comentarios asociados a tareas.

```text
Task 1 ─────── N TaskComment

User 1 ─────── N TaskComment
```

### Tag

Representa etiquetas que pueden asociarse a tareas.

La relación entre `Task` y `Tag` es muchos a muchos:

```text
Task N ─────── N Tag
```

utilizando la tabla intermedia:

```text
task_tags
```

---

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

## Flujo recomendado

Cuando modifiques los modelos:

```text
Modificar models.py
       │
       ▼
alembic revision --autogenerate
       │
       ▼
Revisar migration
       │
       ▼
alembic upgrade head
```

Las migraciones deben revisarse manualmente antes de aplicarlas.

---

# ▶️ Ejecutar la aplicación

Puedes iniciar el servidor con:

```bash
uv run uvicorn app.main:app --reload
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

La aplicación está preparada para incorporar posteriormente:

* password hashing
* autenticación
* JWT
* autorización
* roles/permisos

---

# 🧠 Objetivos de aprendizaje

Este proyecto está diseñado para practicar:

* Python
* FastAPI
* REST APIs
* SQLModel
* SQLAlchemy
* MySQL
* Alembic
* ORM
* relaciones entre entidades
* Dependency Injection
* Repository Pattern
* Service Layer
* validación de datos
* manejo de errores
* autenticación
* testing
* arquitectura backend

---

# 📚 Próximos pasos

Algunas funcionalidades que pueden incorporarse:

* [ ] CRUD completo de usuarios
* [ ] CRUD de proyectos
* [ ] CRUD de tareas
* [ ] CRUD de comentarios
* [ ] CRUD de tags
* [ ] Filtros y paginación
* [ ] Ordenamiento
* [ ] Manejo global de excepciones
* [ ] Autenticación JWT
* [ ] Password hashing
* [ ] Roles y permisos
* [ ] Tests unitarios
* [ ] Tests de integración
* [ ] Docker
* [ ] Docker Compose
* [ ] CI/CD
* [ ] Logging
* [ ] Health check
* [ ] Rate limiting

---

# 📄 License

This project is intended for educational and demonstration purposes.

