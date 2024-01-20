from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    balance = models.FloatField(default=0)
    email = models.EmailField(unique=True, blank=False, null=False)


class Roll(models.Model):
    cost = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    roll_board = models.CharField(max_length=100)
    winings = models.FloatField(default=0)

    @property
    def result(self):
        return self.cost * self.winings
