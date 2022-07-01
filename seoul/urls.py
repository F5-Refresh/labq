from django.urls import path

from .views import SeoulWaterLevelRainFallView

urlpatterns = [path('/gu-search/<str:gu_name>', SeoulWaterLevelRainFallView.as_view())]
