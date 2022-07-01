from django.test import RequestFactory, TestCase
from seoul.views import SeoulWaterLevelRainFallView, dict_gu_id


class SeoulTest(TestCase):
    
	def test_search_result(self):
     
		'''
		date : 2022-06-30
		writer : 남효정
		'''

		url = '127.0.0.1/8000/api/seoul/gu-search'
		factory = RequestFactory()
		view = SeoulWaterLevelRainFallView.as_view()
		request = factory.get(url)
		
		for request_gu_name in dict_gu_id:
     	
			response = view(request, request_gu_name)
   
			# 데이터가 없다면 detail 나옵니다. / detail이 있을 경우, continue로 진행합니다.
			if 'detail' in response.data: 
				continue

			gu_name = response.data['data']['gu_name']
			avg_water_level = response.data['data']['avg_water_level']

			# 검색 데이터와 응답한 데이터가 일치하는지 확인합니다.
			self.assertIsNotNone(avg_water_level)
			self.assertEquals(gu_name, request_gu_name)
			self.assertEquals(response.status_code, 200)
			
			# 올바른 type인지 확인합니다.
			type_gu_name = type(gu_name)
			type_avg_water_level = type(avg_water_level)
   
			assert type_gu_name is str, 'gu_name이 string 타입이 아닙니다.'
			assert type_avg_water_level is float, 'avg_water_level이 float 타입이 아닙니다.'
   
   

			# rainguage_info의 개수는 지역마다 달라서 개수가 다르기 때문에 따로 작성하였습니다.
			raingauge_info = response.data['data']['raingauge_info']
			
			for raingauge_info_index in range(len(raingauge_info)):
				raingauge_name = raingauge_info[raingauge_info_index]['raingauge_name']
				sum_rain_fall = raingauge_info[raingauge_info_index]['sum_rain_fall']
    
				# null 값이 아닌지 확인합니다. (null일 경우 에러 발생)
				self.assertIsNotNone(raingauge_info)
				self.assertIsNotNone(raingauge_name)
				self.assertIsNotNone(sum_rain_fall)
    			
      			 # 올바른 type인지 확인합니다.
				type_raingauge_info = type(raingauge_info)
				type_rainguage_name = type(raingauge_name)
				type_sum_rain_fall = type(sum_rain_fall)
    
				assert type_raingauge_info is list, 'raingauge_info가 list 타입이 아닙니다.'
				assert type_rainguage_name is str, 'rainguage_name이 str 타입이 아닙니다.'
				assert type_sum_rain_fall is float, 'sum_rain_fall이 float 타입이 아닙니다.'
 