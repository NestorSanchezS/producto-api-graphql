"""Serializadores: validan la entrada y dan forma a la salida JSON de la API."""

from rest_framework import serializers

from .models import Producto


class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ["id", "nombre", "descripcion", "precio"]
        read_only_fields = ["id"]

    def validate_precio(self, valor):
        """Manejo de errores de negocio: el precio debe ser mayor que cero."""
        if valor <= 0:
            raise serializers.ValidationError("El precio debe ser mayor que cero.")
        return valor

    def validate_nombre(self, valor):
        if not valor.strip():
            raise serializers.ValidationError("El nombre no puede estar vacío.")
        return valor
