from rest_framework import serializers
# from app1.models import RaceResult, Odds, JoinResultOdds
# class RaceResultSeriralizer(serializers.ModelSerializer):
#     class Meta:
#         model = RaceResult
#         fields = '__all__'

# class OddsSerilizer(serializers.ModelSerializer):
#     class Meta:
#         model = Odds
#         fields = '__all__'

# class RacenameSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = RaceResult
#         fields = ['race_name']

# class JoinResultOddsSerializer(serializers.ModelSerializer):
#     RaceResult = RaceResultSeriralizer(read_only=True)
#     Odds = OddsSerilizer(read_only=True)

#     class Meta:
#         model = JoinResultOdds
#         fields = ["RaceResult", "Odds"]
