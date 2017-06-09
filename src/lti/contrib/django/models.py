from django.db import models


class NonceHistory(models.Model):
    client_key = models.CharField(max_length=200)
    timestamp = models.IntegerField()
    nonce = models.CharField(max_length=200)
