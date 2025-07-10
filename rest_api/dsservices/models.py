from django.db import models

class DustReading(models.Model):
    sensor_id = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    pm10 = models.FloatField()
    pm25 = models.FloatField()
    so2 = models.FloatField()
    no2 = models.FloatField()
    no = models.FloatField()
    co = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    raw_payload = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'dust_read'
    def __str__(self):
        return f"{self.sensor_id} @ {self.timestamp}"