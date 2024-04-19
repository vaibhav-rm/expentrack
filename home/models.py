from django.db import models

# Create your models here.
class History(models.Model):
    desc = models.CharField(max_length=20)
    amount = models.IntegerField()