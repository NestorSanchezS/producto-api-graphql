"""Esquema GraphQL de la entidad Producto (librería: graphene-django).

CRUD completo por GraphQL:
- Queries:    productos (listar) y productoPorId (leer).
- Mutaciones: crearProducto, actualizarProducto, eliminarProducto.

GraphQL permite que el cliente pida exactamente los campos que necesita,
a diferencia de REST donde el servidor define la forma de la respuesta.
"""

import graphene
from graphene_django import DjangoObjectType

from .models import Producto


class ProductoType(DjangoObjectType):
    """Convierte el modelo del ORM en un tipo GraphQL automáticamente."""

    class Meta:
        model = Producto
        fields = ("id", "nombre", "descripcion", "precio")


def _validar(nombre, precio):
    """Validaciones de negocio compartidas por crear y actualizar."""
    if precio <= 0:
        raise Exception("El precio debe ser mayor que cero.")
    if not nombre.strip():
        raise Exception("El nombre no puede estar vacío.")


def _obtener_o_error(id):
    """Busca el producto o lanza un error controlado (manejo de errores)."""
    try:
        return Producto.objects.get(pk=id)
    except Producto.DoesNotExist:
        raise Exception(f"El producto con id {id} no existe.")


class Query(graphene.ObjectType):
    productos = graphene.List(ProductoType, description="Lista todos los productos")
    producto_por_id = graphene.Field(
        ProductoType,
        id=graphene.Int(required=True),
        description="Obtiene un producto por su id",
    )

    def resolve_productos(root, info):
        return Producto.objects.all().order_by("id")

    def resolve_producto_por_id(root, info, id):
        return _obtener_o_error(id)


class CrearProducto(graphene.Mutation):
    """C del CRUD."""

    class Arguments:
        nombre = graphene.String(required=True)
        descripcion = graphene.String(default_value="")
        precio = graphene.Float(required=True)

    producto = graphene.Field(ProductoType)

    def mutate(root, info, nombre, descripcion, precio):
        _validar(nombre, precio)
        producto = Producto.objects.create(
            nombre=nombre, descripcion=descripcion, precio=precio
        )
        return CrearProducto(producto=producto)


class ActualizarProducto(graphene.Mutation):
    """U del CRUD."""

    class Arguments:
        id = graphene.Int(required=True)
        nombre = graphene.String(required=True)
        descripcion = graphene.String(default_value="")
        precio = graphene.Float(required=True)

    producto = graphene.Field(ProductoType)

    def mutate(root, info, id, nombre, descripcion, precio):
        producto = _obtener_o_error(id)
        _validar(nombre, precio)
        producto.nombre = nombre
        producto.descripcion = descripcion
        producto.precio = precio
        producto.save()
        return ActualizarProducto(producto=producto)


class EliminarProducto(graphene.Mutation):
    """D del CRUD."""

    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    mensaje = graphene.String()

    def mutate(root, info, id):
        producto = _obtener_o_error(id)
        producto.delete()
        return EliminarProducto(ok=True, mensaje=f"Producto {id} eliminado correctamente.")


class Mutation(graphene.ObjectType):
    crear_producto = CrearProducto.Field()
    actualizar_producto = ActualizarProducto.Field()
    eliminar_producto = EliminarProducto.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
