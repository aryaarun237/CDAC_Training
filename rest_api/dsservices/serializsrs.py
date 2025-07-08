from rest_framework import serializers
from .models import DustReading

class DustReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DustReading
        fields = '__all__'
