from django.db import models
from django.contrib.auth.models import AbstractUser
from json import loads

# Create your models here.
class User(AbstractUser):
    balance = models.FloatField(default=0)
    email = models.EmailField(unique=False, blank=True, null=True)


class Roll(models.Model):
    cost = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    board_info = models.JSONField(null=False, default='dict')
    winings_multyplier = models.FloatField(default=0)

    @property
    def result(self):
        return self.cost * self.winings_multyplier
    

