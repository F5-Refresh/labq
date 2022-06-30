from django.urls import path, include

urlpatterns = [
    path('api/seoul', include('seoul.urls')),
]