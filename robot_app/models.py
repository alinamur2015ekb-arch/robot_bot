from django.db import models

class Telemetry(models.Model):
    temperatura = models.FloatField()
    humdiet = models.FloatField()
    status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.timestamp} - Temp: {self.temp}, Status: {self.status}"