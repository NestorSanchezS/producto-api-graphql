"""Rutas principales del proyecto."""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


def raiz(_request):
    return JsonResponse(
        {
            "mensaje": "API de Productos - Arquitectura de Aplicaciones Web (Unidad 2)",
            "endpoints": [
                "GET    /api/productos/",
                "GET    /api/productos/{id}/",
                "POST   /api/productos/",
                "PUT    /api/productos/{id}/",
                "DELETE /api/productos/{id}/",
            ],
        }
    )


urlpatterns = [
    path("", raiz),
    path("admin/", admin.site.urls),
    path("api/", include("productos.urls")),
    # Endpoint GraphQL con interfaz GraphiQL en el navegador
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]
