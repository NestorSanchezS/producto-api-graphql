# API RESTful de Productos — Django + Django REST Framework

Backend con servicios RESTful CRUD sobre base de datos, desarrollado para la **Unidad 2** del módulo **Arquitectura de Aplicaciones Web** (Politécnico Grancolombiano).

## Tecnologías

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.10+ |
| Framework backend | Django (mencionado explícitamente en la guía de la actividad) |
| API REST | Django REST Framework (DRF) |
| ORM | Django ORM (crea la tabla vía migraciones, sin SQL manual) |
| Base de datos | SQLite local (por defecto; configurable a PostgreSQL en `settings.py`) |
| Pruebas en navegador | API navegable de DRF en `/api/productos/` |

## Arquitectura del proyecto

Estructura estándar de Django (proyecto + app), con responsabilidades separadas por archivo:

```
producto-api-django/
├── manage.py
├── requirements.txt
├── producto_api/            # Configuración del proyecto
│   ├── settings.py          # Apps instaladas, base de datos
│   └── urls.py              # Rutas principales (incluye /api/)
└── productos/               # App de la entidad Producto
    ├── models.py            # Entidad Producto (id, nombre, descripcion, precio) — Django ORM
    ├── serializers.py       # Validación de entrada/salida (precio > 0, nombre no vacío)
    ├── views.py             # ProductoViewSet: endpoints CRUD y manejo de errores
    ├── urls.py              # Router de DRF que genera las rutas REST
    └── migrations/          # Migraciones generadas por el ORM
```

## Ejecución

```bash
# 1. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Crear la base de datos con el ORM (migraciones, sin SQL manual)
python manage.py migrate

# 4. Ejecutar
python manage.py runserver
```

- API: `http://localhost:8000/api/productos/`
- **API navegable de DRF** (interfaz web para probar GET/POST/PUT/DELETE desde el navegador): la misma URL.

## Endpoints

| Método | Ruta | Descripción | Éxito |
|---|---|---|---|
| GET | `/api/productos/` | Listar todos los productos | 200 |
| GET | `/api/productos/{id}/` | Obtener un producto por id | 200 |
| POST | `/api/productos/` | Crear un producto | 201 |
| PUT | `/api/productos/{id}/` | Actualizar un producto | 200 |
| DELETE | `/api/productos/{id}/` | Eliminar un producto | 200 |

> Nota: en Django las rutas terminan en `/` (barra final obligatoria).

## Manejo de errores

| Caso | Código | Respuesta |
|---|---|---|
| Producto inexistente (GET/PUT/DELETE) | 404 | `{"detail": "El producto con id X no existe."}` |
| Precio ≤ 0 | 400 | `{"precio": ["El precio debe ser mayor que cero."]}` |
| Precio o nombre faltante | 400 | `{"precio": ["This field is required."]}` |
| Error inesperado de base de datos | 500 | Mensaje controlado |

## Pruebas rápidas con curl

```bash
# POST — crear
curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Teclado mecánico","descripcion":"Switches rojos, RGB","precio":250000}'

# GET — listar / por id
curl http://localhost:8000/api/productos/
curl http://localhost:8000/api/productos/1/

# PUT — actualizar
curl -X PUT http://localhost:8000/api/productos/1/ \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Teclado mecánico TKL","descripcion":"Sin numpad","precio":220000}'

# DELETE — eliminar
curl -X DELETE http://localhost:8000/api/productos/1/

# Errores
curl http://localhost:8000/api/productos/999/                    # 404
curl -X POST http://localhost:8000/api/productos/ \
  -H "Content-Type: application/json" -d '{"nombre":"X","precio":-5}'   # 400
```

## Base de datos en la nube (opcional)

Para usar un PostgreSQL gratuito de Supabase o Render, en `producto_api/settings.py` reemplaza `DATABASES` por:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "postgres",
        "USER": "usuario",
        "PASSWORD": "password",
        "HOST": "host-de-supabase",
        "PORT": "5432",
    }
}
```

e instala el driver: `pip install psycopg2-binary`.

## Subir a GitHub

```bash
git init
git add .
git commit -m "API RESTful CRUD de Productos con Django + DRF"
git branch -M main
git remote add origin https://github.com/<tu-usuario>/producto-api-django.git
git push -u origin main
```

---

## GraphQL (Unidad 3)

Integración de GraphQL con la librería **graphene-django** sobre el mismo proyecto.

```bash
pip install graphene-django
```

Configuración realizada:
1. `graphene_django` agregado a `INSTALLED_APPS` y bloque `GRAPHENE` en `settings.py` apuntando al esquema.
2. `productos/schema.py` → `ProductoType` (generado desde el modelo del ORM), queries `productos` y `productoPorId`, y mutación `crearProducto`.
3. Ruta `/graphql/` en `producto_api/urls.py` con la interfaz **GraphiQL** habilitada.

Probar en el navegador: `http://localhost:8000/graphql/`

```graphql
# Consulta declarativa: solo los campos que el cliente necesita
{
  productos {
    nombre
    precio
  }
}

# Por id
{
  productoPorId(id: 1) {
    id
    nombre
    descripcion
    precio
  }
}

# Mutaciones (CRUD completo)
mutation {
  crearProducto(nombre: "Teclado mecánico", descripcion: "Switches rojos", precio: 250000) {
    producto { id nombre precio }
  }
}
```

```graphql
mutation {
  actualizarProducto(id: 1, nombre: "Teclado TKL", descripcion: "Sin numpad", precio: 220000) {
    producto { id nombre precio }
  }
}

mutation {
  eliminarProducto(id: 1) {
    ok
    mensaje
  }
}
```
