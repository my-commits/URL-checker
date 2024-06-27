from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import URLViewSet

router = DefaultRouter()
router.register(r'urls', URLViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
