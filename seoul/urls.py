from django.urls import path

from .views import SeoulSewerLevelRainFallView

urlpatterns = [path('/gu-search/<str:gu_name>', SeoulSewerLevelRainFallView.as_view())]
