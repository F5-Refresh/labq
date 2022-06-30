from django.urls import path
from seoul.views import OpenApiDataView

urlpatterns = [
    path('/gu-search', OpenApiDataView.as_view())
]