from rest_framework             import serializers
from rest_framework.serializers import Serializer


class SewerPipeSerializer(Serializer):
    IDN     = serializers.CharField()
    GUBN    = serializers.CharField()
    MEA_YMD = serializers.DateTimeField()
    MEA_WAL = serializers.FloatField()
    SIG_STA = serializers.CharField()
    

class RainFallSerializer(Serializer):
    RAINGAUGE_CODE = serializers.FloatField()
    RAINGAUGE_NAME = serializers.CharField()
    GU_CODE        = serializers.FloatField()
    GU_NAME        = serializers.CharField()
    RAINFALL10     = serializers.FloatField()
    RECEIVE_TIME   = serializers.DateTimeField()