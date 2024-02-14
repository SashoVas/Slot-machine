from rest_framework import serializers
from machine.models import User
from machine.models import Roll

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name","balance"]

class RollSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roll
        fields = ["id", "cost", "time", "user","board_info","winings_multyplier", "result","scatter_multiplier"]
