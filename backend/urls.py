from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),

    # frontend entry point
    re_path(r'^$', TemplateView.as_view(template_name="index.html"), name="frontend"),

    # # backend: authorization
    path('openid/', include('openid.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('auth/', include('djoser.urls.jwt')),

    # backend: api
    path('api/v1/', include('api.urls')),
]
