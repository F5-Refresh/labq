from rest_framework import serializers


class SeoulSewerLevel(serializers.Serializer):
    IDN = serializers.IntegerField()
    GUBN = serializers.CharField(max_length=10)
    GUBN_NAM = serializers.CharField(max_length=50)
    MEA_YMD = serializers.DateTimeField()
    MEA_WAL = serializers.FloatField()


class SeoulRainGauge(serializers.Serializer):
    raingauge_name = serializers.CharField(max_length=50)
    sum_rain_fall = serializers.FloatField()


class SeoulSewerLevelRainFall(serializers.Serializer):
    gu_name = serializers.CharField(max_length=20)
    avg_water_level = serializers.FloatField()

    raingauge_info = SeoulRainGauge(many=True)
