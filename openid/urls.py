from django.urls import path
from . import views

app_name = 'openid'
urlpatterns = [
    path('login/<str:realm>/', views.open_id, name='login'),
    path('callback/', views.open_id_callback, name='callback')
]