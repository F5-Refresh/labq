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
		
		for request_gu_name in dict_gu_id.keys():
		
			response = view(request, request_gu_name)
			gu_name = response.data['data']['gu_name']

			avg_water_level = response.data['data']['avg_water_level']
			raingauge_info = response.data['data']['raingauge_info']
			rainguage_name = response.data['data']['raingauge_info'][0]['raingauge_name']
			sum_rain_fall = response.data['data']['raingauge_info'][0]['sum_rain_fall']

			# 검색 데이터와 응답 데이터가 동일한지 확인합니다.			
			self.assertEquals(gu_name, request_gu_name)
			self.assertEquals(response.status_code, 200)
   
			# null 값이 아닌지 확인합니다. (null일 경우 에러 발생)
			self.assertIsNotNone(avg_water_level)
			self.assertIsNotNone(raingauge_info)
			self.assertIsNotNone(rainguage_name)
			self.assertIsNotNone(sum_rain_fall)