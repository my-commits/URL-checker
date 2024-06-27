from django.db import models
from django.contrib.auth.models import User


class URL(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    url = models.URLField()
    status_code = models.IntegerField(null=True, blank=True)
    last_checked = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.url
