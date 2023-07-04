from rest_framework import serializers
from app1.models import RaceResult, Odds

class RaceResultSeriralizer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = '__all__'

class OddsSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Odds
        fields = '__all__'

class RacenameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RaceResult
        fields = ['race_name']