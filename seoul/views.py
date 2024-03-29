import json
import os
import re
import statistics
from datetime import datetime, timedelta
from itertools import groupby

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from seoul.serializers import SeoulWaterLevelRainFall

dict_gu_id = {
    '종로구': '01',
    '중구': '02',
    '용산구': '03',
    '성동구': '04',
    '광진구': '05',
    '동대문구': '06',
    '중랑구': '07',
    '성북구': '08',
    '강북구': '09',
    '도봉구': '10',
    '노원구': '11',
    '은평구': '12',
    '서대문구': '13',
    '마포구': '14',
    '양천구': '15',
    '강서구': '16',
    '구로구': '17',
    '금천구': '18',
    '영등포구': '19',
    '동작구': '20',
    '관악구': '21',
    '서초구': '22',
    '강남구': '23',
    '송파구': '24',
    '강동구': '25',
}

OPEN_API_KEY = os.environ.get('OPEN_API_SECRET_KEY')


# Create your views here.
class SeoulWaterLevelRainFallView(APIView):
    """
    date : 2022-06-30
    writer : 조병민
    """

    def get(self, request, gu_name):

        now = datetime.now()
        before_onehour_date = (now - timedelta(hours=1)).strftime('%Y%m%d%H')

        """
        RainFall GET API
        """
        rainfall_URL = f'http://openapi.seoul.go.kr:8088/{OPEN_API_KEY}/json/ListRainfallService/1/100/{gu_name}'
        rainfall_response = json.loads(requests.get(rainfall_URL).content)

        if not 'ListRainfallService' in rainfall_response:
            return Response({'detail': 'Not Found Data'}, status=status.HTTP_200_OK)

        rainfall_data = rainfall_response['ListRainfallService']['row']

        """
        WaterLevel GET API
        """
        gu_id = dict_gu_id[gu_name]

        waterlevel_URL = f'http://openAPI.seoul.go.kr:8088/{OPEN_API_KEY}/json/DrainpipeMonitoringInfo/1/1000/{gu_id}/{before_onehour_date}/{before_onehour_date}'
        waterlevel_response = json.loads(requests.get(waterlevel_URL).content)

        if not 'DrainpipeMonitoringInfo' in waterlevel_response:
            return Response({'detail': 'Not Found Data'}, status=status.HTTP_200_OK)

        waterlevel_data = waterlevel_response['DrainpipeMonitoringInfo']['row']

        """
        Group by
        """
        rainfall_groupby_raingauge = groupby(
            sorted(rainfall_data, key=lambda x: x['RAINGAUGE_CODE']),
            lambda x: x['RAINGAUGE_NAME'],
        )

        """
        RainFallData
        """
        rainfall_by_raingauge_dict = {
            i: round(sum(map(
                        lambda x: float(x['RAINFALL10']) 
                        if re.sub('[-:\s]', '', x['RECEIVE_TIME'])[:10] == before_onehour_date else 0, 
                        j)
                    ),
                2,)
            for i, j in rainfall_groupby_raingauge
        }

        rainfall_by_raingauge = []

        for i, j in rainfall_by_raingauge_dict.items():
            rainfall_by_raingauge.append({'raingauge_name': i, 'sum_rain_fall': j})
            
        """
        WaterLevelData
        """
        waterlevel_by_hour = round(statistics.mean([i['MEA_WAL'] for i in waterlevel_data]), 2)

        data = {
            'gu_name': gu_name,
            'avg_water_level': waterlevel_by_hour,
            'raingauge_info': rainfall_by_raingauge,
        }
        serializer = SeoulWaterLevelRainFall(data=data)

        if not serializer.is_valid():
            Response({'detail': 'Server Error!'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'data': serializer.data}, status=status.HTTP_200_OK)
