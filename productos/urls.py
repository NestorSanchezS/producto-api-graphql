"""Rutas de la app productos: el router de DRF genera los endpoints CRUD."""

from rest_framework.routers import DefaultRouter

from .views import ProductoViewSet

router = DefaultRouter()
router.register("productos", ProductoViewSet, basename="producto")

urlpatterns = router.urls
