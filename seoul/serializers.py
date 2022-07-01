from rest_framework import serializers


class SeoulRainGauge(serializers.Serializer):
    raingauge_name = serializers.CharField(max_length=50)
    sum_rain_fall = serializers.FloatField()


class SeoulWaterLevelRainFall(serializers.Serializer):
    gu_name = serializers.CharField(max_length=20)
    avg_water_level = serializers.FloatField()

    raingauge_info = SeoulRainGauge(many=True)
