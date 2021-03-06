from rest_framework import routers
from . import views

# router = routers.DefaultRouter()

# Sample:
# router.register('players', views.PlayerViewSet, basename='players')

# urlpatterns = router.urls

# for testing/setup:
from django.urls import path, include
urlpatterns = [
    path('test/', views.test_json),
    path('players/', include('players.urls')),
    path('clans/', include('clans.urls')),
]