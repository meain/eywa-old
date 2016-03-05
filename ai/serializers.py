from rest_framework import serializers

from models import Querry

class AiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Querry
