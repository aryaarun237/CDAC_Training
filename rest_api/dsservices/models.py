from django.db import models

class DustReading(models.Model):
    sensor_id = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    dust_level = models.IntegerField()
    temperature = models.IntegerField()
    
    class Meta:
        db_table = 'dust_read'
    def __str__(self):
        return f"{self.sensor_id} @ {self.timestamp}"