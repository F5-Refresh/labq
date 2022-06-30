import requests, datetime, json, statistics, operator, itertools

from rest_framework.views    import APIView
from rest_framework.response import Response

from seoul.serializers import SewerPipeSerializer, RainFallSerializer
from labq.settings     import OPEN_API_SECRET_KEY


class OpenApiDataView(APIView):
    def get(self, request):
        try:
            gu_name = request.GET.get('gu_name', None)  # 구 이름         
            
            if not gu_name:
                return Response({'detail' : 'GUBN_NAM is required'}, status=400)
            
            gubn_nam_set = {
                '종로' : '01', '중' : '02', '용산' : '03', '성동' : '04', '광진' : '05',
                '동대문' : '06', '중랑' : '07', '성북' : '08', '강북' : '09', '도봉' : '10',
                '노원' : '11', '은평' : '12', '서대문' : '13', '마포' : '14', '양천' : '15',
                '강서' : '16', '구로' : '17', '금천' : '18', '영등포' : '19', '동작' : '20',
                '관악' : '21', '서초' : '22', '강남' : '23', '송파' : '24', '강동' : '25'
            }
            
            # 하수관로 Open API 요청 시점 : 현 시점부터 1시간 전의 데이터('YYYY-MM-DD-HH')    
            now = (datetime.datetime.now().strftime('%Y%m%d%H'))
            one_hour_before = (datetime.datetime.now() - datetime.timedelta(hours=1)).strftime('%Y%m%d%H')
            
            sewer_pipe_open_api_url = f"http://openapi.seoul.go.kr:8088/{OPEN_API_SECRET_KEY}/json/DrainpipeMonitoringInfo/1/1000/{gubn_nam_set[gu_name]}/{one_hour_before}/{now}"
            rainfall_api_url        = f"http://openapi.seoul.go.kr:8088/{OPEN_API_SECRET_KEY}/json/ListRainfallService/1/28/{gu_name}"
            
            sewer_pipe_res = json.loads(requests.get(sewer_pipe_open_api_url).content)
            rainfall_res   = json.loads(requests.get(rainfall_api_url).content)
            
            sewer_pipe_datas = sewer_pipe_res['DrainpipeMonitoringInfo']['row']
            rainfall_datas   = rainfall_res['ListRainfallService']['row']
            
            sewer_pipe_serializer = SewerPipeSerializer(sewer_pipe_datas, many=True)
            rainfall_serializer   = RainFallSerializer(rainfall_datas, many=True)
            
            # 특정 구의 하수관로 평균 수위
            total_avg_sewer_pipe_level = round(
                                               statistics.mean(
                                               [sewer_pipe_data['MEA_WAL']\
                                               for sewer_pipe_data in sewer_pipe_serializer.data\
                                               if int(sewer_pipe_data['MEA_YMD'][11:13]) < int(datetime.datetime.now().strftime('%H'))]), 3)

            rainfall_sorted_data  = sorted(rainfall_serializer.data, key=operator.itemgetter('RAINGAUGE_NAME'))
            rainfall_grouped_data = itertools.groupby(rainfall_sorted_data, key=operator.itemgetter('RAINGAUGE_NAME'))
            
            result = {}
            
            for key, group_data in rainfall_grouped_data:
                result[key] = list(group_data)
            
            rainguage_info = []    

            # 특정 구의 raingauge별 총 강우량(합계)
            for key, datas in result.items():
                sum_raingauge_rainfall = {key : {'sum_rainfall' : sum([data['RAINFALL10'] for data in datas\
                                                                  if int(datetime.datetime.now().strftime('%H'))-1\
                                                                     <= int(data['RECEIVE_TIME'][11:13])\
                                                                     < int(datetime.datetime.now().strftime('%H'))])}}
                rainguage_info.append(sum_raingauge_rainfall)
            
            total_data = {
                gu_name : {
                    'totalavg_sewer_pipe_level' : total_avg_sewer_pipe_level,
                },
                'raingauge_info' : rainguage_info,
            }
                    
            return Response({'data' : total_data}, status=200)
        
        except KeyError:
            return Response({'detail' : 'key error'}, status=400)
        except json.JSONDecodeError:
            return Response({'detail' : 'json decode error'}, status=400)