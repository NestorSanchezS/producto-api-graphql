"""Modelo ORM de la entidad Producto.

El ORM de Django crea la tabla "productos" a partir de esta clase mediante
las migraciones (makemigrations / migrate), sin escribir SQL manual.
"""

from django.db import models


class Producto(models.Model):
    # id: Django lo crea automáticamente como clave primaria autoincremental.
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, default="")
    precio = models.FloatField()

    class Meta:
        db_table = "productos"

    def __str__(self):
        return f"{self.nombre} (${self.precio})"
