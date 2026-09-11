"""Vistas de la API RESTful de Productos.

ModelViewSet de Django REST Framework expone los endpoints CRUD:
- GET    /api/productos/        -> list
- POST   /api/productos/        -> create   (201)
- GET    /api/productos/{id}/   -> retrieve (404 si no existe)
- PUT    /api/productos/{id}/   -> update
- DELETE /api/productos/{id}/   -> destroy

Manejo de errores:
- 404 con mensaje claro si el producto no existe.
- 400 si el body es inválido (nombre vacío, precio faltante o <= 0).
- 500 controlado ante errores inesperados de base de datos.
"""

from django.db import DatabaseError
from django.http import Http404
from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import Producto
from .serializers import ProductoSerializer


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all().order_by("id")
    serializer_class = ProductoSerializer

    def get_object(self):
        """Personaliza el 404 con un mensaje en español."""
        try:
            return super().get_object()
        except Http404:
            raise Http404(f"El producto con id {self.kwargs.get('pk')} no existe.")

    def destroy(self, request, *args, **kwargs):
        """DELETE con mensaje de confirmación en lugar de un 204 vacío."""
        producto = self.get_object()
        producto_id = producto.id
        try:
            producto.delete()
        except DatabaseError:
            return Response(
                {"error": "Error al eliminar el producto."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return Response(
            {"mensaje": f"Producto {producto_id} eliminado correctamente."},
            status=status.HTTP_200_OK,
        )
