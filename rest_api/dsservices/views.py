from rest_framework import viewsets
from .models import DustReading
from .serializsrs import DustReadingSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class DustReadingViewSet(viewsets.ModelViewSet):
    queryset = DustReading.objects.all()
    serializer_class = DustReadingSerializer

    @action(detail=False, methods=['get'])
    def high_readings(self, request):
        high_readings = DustReading.objects.filter(dust_level__gt=300)
        serializer = self.get_serializer(high_readings, many=True)
        return Response(serializer.data)
