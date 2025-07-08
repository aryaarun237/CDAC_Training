from django.urls import path, include
from rest_framework import routers
from .views import DustReadingViewSet

router = routers.DefaultRouter()
router.register(r'readings', DustReadingViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
