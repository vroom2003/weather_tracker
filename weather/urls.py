from django.urls import path
from . import views

urlpatterns = [
    path('debug/', views.debug_env, name='debug'),
    path('test-api/', views.test_api_key, name='test_api'),
    path('', views.weather_view, name='weather'),
]