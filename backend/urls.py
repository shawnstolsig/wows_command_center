from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    # admin page
    path('admin/', admin.site.urls),

    # frontend entry point
    re_path(r'^$', TemplateView.as_view(template_name="index.html")),

    # # backend: authorization
    # path('auth/', include('djoser.urls')),
    # path('auth/', include('djoser.urls.jwt')),

    # backend: api
    path('api/v1/', include('api.urls'))
]
