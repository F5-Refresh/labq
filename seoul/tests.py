from django.test import RequestFactory, TestCase
from seoul.views import SeoulWaterLevelRainFallView, dict_gu_id ,OPEN_API_KEY
import json , requests


class SeoulTest(TestCase):
    
	'''
	date : 2022-06-30
	writer : 남효정
	'''

	def test_search_result(self):

		url = '127.0.0.1/8000/api/seoul/gu-search'
		factory = RequestFactory()
		view = SeoulWaterLevelRainFallView.as_view()
		request = factory.get(url)
		
		for request_gu_name in dict_gu_id.keys():
     	
			response = view(request, request_gu_name)
   
			# 데이터가 없다면 detail 나옴 / detail이 없을 경우, continue
			if 'detail' in response.data: 
				continue

			gu_name = response.data['data']['gu_name']
			avg_water_level = response.data['data']['avg_water_level']
			raingauge_info = response.data['data']['raingauge_info']
			rainguage_name = response.data['data']['raingauge_info'][0]['raingauge_name']
			sum_rain_fall = response.data['data']['raingauge_info'][0]['sum_rain_fall']
   
			
			# 검색 데이터와 응답한 데이터가 일치하는지 확인합니다.
			self.assertEquals(gu_name, request_gu_name)
			self.assertEquals(response.status_code, 200)
   
			# null 값이 아닌지 확인합니다. (null일 경우 에러 발생)
			self.assertIsNotNone(avg_water_level)
			self.assertIsNotNone(raingauge_info)
			self.assertIsNotNone(rainguage_name)
			self.assertIsNotNone(sum_rain_fall)

	'''
    date : 2022-06-30
    writer : 전기원
    '''

	# view api의 우량계 리스트와 open api의 우량계 리스트가 동일한지 테스트하는 코드입니다.
	def test_get_gauge(self):
		gu_name = '종로구'

		#view api의 우량계 리스트를 가져오는 코드입니다.
		url = 'http://127.0.0.1:8000/api/seoul/gu-search/'
		factory = RequestFactory()
		view = SeoulWaterLevelRainFallView.as_view()
		request = factory.get(url, format = 'json')
		response = view(request, gu_name)
		self.assertEqual(response.status_code, 200)
		
		gauge_list = []
		for info in response.data['data']['raingauge_info']:
      
			# 데이터가 없다면 detail이 나옴. detail이 없을 경우, continue합니다.
			if 'detail' in response.data: 
				continue
			gauge_list.append(info['raingauge_name'])


		# open api에서 우량계 리스트를 가져오는 코드 입니다.
		rainfall_URL = f'http://openapi.seoul.go.kr:8088/{OPEN_API_KEY}/json/ListRainfallService/1/100/{gu_name}'
		rainfall_response = json.loads(requests.get(rainfall_URL).content)
		
		open_gauge_list = set()
		for info in rainfall_response['ListRainfallService']['row']:
			open_gauge_list.add(info['RAINGAUGE_NAME'])
		open_gauge_list = list(open_gauge_list)
				
		# 두 리스트의 요소들을 정렬합니다.
		gauge_list.sort()
		open_gauge_list.sort()
				
		# 유닛테스트에서 두 리스트의 값이 동일한지 확인합니다.
		self.assertEqual(open_gauge_list, gauge_list)
