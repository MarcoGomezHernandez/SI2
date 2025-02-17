from rest_framework.routers import DefaultRouter
from .api import CensoViewSet, VotoViewSet

router = DefaultRouter()
router.register(r'censos', CensoViewSet)
router.register(r'votos', VotoViewSet)

urlpatterns = router.urls
