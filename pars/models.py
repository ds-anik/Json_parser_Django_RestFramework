from django.db import models


class Log(models.Model):
    data = models.JSONField()

    def __str__(self):
        return self.data
